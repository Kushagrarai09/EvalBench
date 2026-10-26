import io, json, os
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .database import Base, engine, get_db
from .models import Task, now
from .schemas import TaskCreate, AnnotationUpdate
load_dotenv(Path(__file__).resolve().parents[1]/".env")
Base.metadata.create_all(bind=engine)
app=FastAPI(title="EvalBench API",version="1.0.0",description="Human text annotation, response ranking, and dataset QA")
origins=[x.strip() for x in os.getenv("FRONTEND_ORIGINS","http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
LABELS=["sentiment","intent","relevance","text_quality"]
RATINGS=["a_accuracy","a_relevance","a_clarity","a_instruction_following","b_accuracy","b_relevance","b_clarity","b_instruction_following"]
VALID={"sentiment":{"positive","negative","neutral"},"intent":{"question","complaint","request","feedback","other"},"relevance":{"relevant","irrelevant"},"text_quality":{"clear","unclear"},"preferred_response":{"A","B","tie","both_bad"},"error_category":{"none","factual_error","hallucination","irrelevant","instruction_following","unsafe","poor_clarity","other"}}
def dump(t):
    d={c.name:getattr(t,c.name) for c in Task.__table__.columns}
    for k in ("created_at","updated_at"): d[k]=d[k].isoformat() if d[k] else None
    return d
def qa(db):
    tasks=db.query(Task).order_by(Task.id).all(); issues=[]; seen={}
    for t in tasks:
        norm=" ".join((t.prompt or "").lower().split())
        if norm and norm in seen: issues.append({"task_id":t.id,"severity":"warning","code":"duplicate_prompt","message":f"Prompt duplicates task #{seen[norm]}."})
        elif norm: seen[norm]=t.id
        if t.status=="completed":
            missing=[f for f in LABELS+RATINGS+["preferred_response"] if getattr(t,f) is None]
            if not (t.rationale or "").strip(): missing.append("rationale")
            if missing: issues.append({"task_id":t.id,"severity":"error","code":"incomplete_annotation","message":"Missing: "+", ".join(missing)})
        for f,choices in VALID.items():
            v=getattr(t,f,None)
            if v is not None and v not in choices: issues.append({"task_id":t.id,"severity":"error","code":"invalid_label","message":f"Invalid {f}: {v}"})
        for f in RATINGS:
            v=getattr(t,f)
            if v is not None and not 1<=v<=5: issues.append({"task_id":t.id,"severity":"error","code":"invalid_rating","message":f"{f} must be 1–5."})
    return issues
@app.get("/api/health")
def health(): return {"status":"ok","service":"EvalBench API"}
@app.get("/api/dashboard")
def dashboard(db:Session=Depends(get_db)):
    ts=db.query(Task).all(); total=len(ts); done=sum(t.status=="completed" for t in ts); review=sum(t.status=="in_review" for t in ts); pending=sum(t.status=="pending" for t in ts); prefs={k:sum(t.preferred_response==k for t in ts) for k in ["A","B","tie","both_bad"]}; completed=[t for t in ts if t.status=="completed"]
    return {"total_tasks":total,"completed":done,"pending":pending,"in_review":review,"completion_rate":round(done/total*100,1) if total else 0,"review_rate":round(review/total*100,1) if total else 0,"error_rate":round(sum(bool(t.error_category and t.error_category!="none") for t in completed)/len(completed)*100,1) if completed else 0,"qa_issue_count":len(qa(db)),"preference_distribution":prefs,"recent_tasks":[dump(t) for t in sorted(ts,key=lambda t:t.updated_at or t.created_at,reverse=True)[:5]]}
@app.get("/api/tasks")
def list_tasks(status:str|None=None,search:str|None=None,db:Session=Depends(get_db)):
    q=db.query(Task)
    if status and status!="all": q=q.filter(Task.status==status)
    if search: q=q.filter(Task.prompt.ilike(f"%{search.strip()}%"))
    return [dump(t) for t in q.order_by(Task.updated_at.desc(),Task.id.desc()).all()]
@app.post("/api/tasks",status_code=201)
def create_task(p:TaskCreate,db:Session=Depends(get_db)):
    if not p.prompt.strip(): raise HTTPException(422,"Prompt cannot be blank")
    t=Task(prompt=p.prompt.strip(),text=p.text.strip(),response_a=p.response_a.strip(),response_b=p.response_b.strip(),source=p.source.strip() or "manual")
    db.add(t);db.commit();db.refresh(t);return dump(t)
@app.get("/api/tasks/{task_id}")
def get_task(task_id:int,db:Session=Depends(get_db)):
    t=db.get(Task,task_id)
    if not t: raise HTTPException(404,"Task not found")
    return dump(t)
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id:int,db:Session=Depends(get_db)):
    t=db.get(Task,task_id)
    if not t: raise HTTPException(404,"Task not found")
    db.delete(t);db.commit();return {"deleted":True,"id":task_id}
@app.put("/api/tasks/{task_id}/annotation")
def save_annotation(task_id:int,p:AnnotationUpdate,db:Session=Depends(get_db)):
    t=db.get(Task,task_id)
    if not t: raise HTTPException(404,"Task not found")
    fields=p.model_dump(exclude_unset=True); requested=fields.pop("status",None)
    for k,v in fields.items(): setattr(t,k,v)
    missing=[f for f in LABELS+RATINGS+["preferred_response"] if getattr(t,f) is None]
    if not (t.rationale or "").strip(): missing.append("rationale")
    if requested=="completed" and missing: raise HTTPException(422,{"message":"Required fields are missing.","missing_fields":missing})
    if requested: t.status=requested
    else: t.status="completed" if not missing else "in_review"
    t.updated_at=now();db.commit();db.refresh(t);return dump(t)
@app.get("/api/qa/issues")
def qa_issues(db:Session=Depends(get_db)):
    xs=qa(db);return {"count":len(xs),"errors":sum(x["severity"]=="error" for x in xs),"warnings":sum(x["severity"]=="warning" for x in xs),"issues":xs}
@app.post("/api/datasets/import")
async def import_dataset(file:UploadFile=File(...),db:Session=Depends(get_db)):
    raw=await file.read(); name=(file.filename or "").lower()
    try:
        if name.endswith(".json"):
            data=json.loads(raw.decode("utf-8-sig")); data=data.get("data",data.get("tasks",[])) if isinstance(data,dict) else data
            if not isinstance(data,list): raise ValueError("JSON must contain a list of task objects")
            df=pd.DataFrame(data)
        elif name.endswith(".csv"): df=pd.read_csv(io.BytesIO(raw)).fillna("")
        else: raise HTTPException(400,"Upload a .csv or .json file")
        if "prompt" not in df.columns: raise ValueError("Required 'prompt' column is missing")
        added=skipped=0
        for _,r in df.iterrows():
            prompt=str(r.get("prompt","")).strip()
            if not prompt: skipped+=1;continue
            db.add(Task(prompt=prompt,text=str(r.get("text","") or ""),response_a=str(r.get("response_a","") or ""),response_b=str(r.get("response_b","") or ""),source=str(r.get("source","import") or "import")));added+=1
        db.commit();return {"added":added,"skipped":skipped,"message":f"Imported {added} tasks; skipped {skipped} rows without prompts."}
    except HTTPException: raise
    except Exception as e: db.rollback();raise HTTPException(400,f"Could not import dataset: {e}")
@app.get("/api/datasets/export")
def export_dataset(format:str=Query("json",pattern="^(json|csv)$"),db:Session=Depends(get_db)):
    rows=[dump(t) for t in db.query(Task).order_by(Task.id).all()]
    if format=="json": content=json.dumps(rows,ensure_ascii=False,indent=2);return StreamingResponse(io.BytesIO(content.encode()),media_type="application/json",headers={"Content-Disposition":"attachment; filename=evalbench_dataset.json"})
    s=io.StringIO();pd.DataFrame(rows).to_csv(s,index=False);return StreamingResponse(io.BytesIO(s.getvalue().encode("utf-8-sig")),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=evalbench_dataset.csv"})
