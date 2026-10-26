from app.database import Base,engine,SessionLocal
from app.models import Task
Base.metadata.create_all(bind=engine); db=SessionLocal()
samples=[
("What is the capital of France?","Paris is the capital of France.","Lyon is the capital of France."),
("Explain RAM versus ROM in simple terms.","RAM is temporary working memory. ROM stores instructions that generally remain without power.","RAM permanently stores photos while ROM is temporary memory for apps."),
("How can I make a password safer?","Use a long, unique password for each account and enable multi-factor authentication.","Use the same short password everywhere."),
("Write a polite response to a delayed delivery complaint.","I'm sorry your order is delayed. I'll check its status and update you.","Delays happen. Just wait.")]
try:
 existing={x[0] for x in db.query(Task.prompt).all()}
 for p,a,b in samples:
  if p not in existing: db.add(Task(prompt=p,text=p,response_a=a,response_b=b,source="demo"))
 db.commit();print(f"Seed complete: {db.query(Task).count()} tasks.")
finally: db.close()
