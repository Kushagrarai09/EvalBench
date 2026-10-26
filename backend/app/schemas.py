from typing import Literal, Optional
from pydantic import BaseModel, Field
class TaskCreate(BaseModel):
    prompt:str=Field(min_length=1,max_length=12000); text:str=""; response_a:str=""; response_b:str=""; source:str="manual"
class AnnotationUpdate(BaseModel):
    sentiment:Optional[Literal["positive","negative","neutral"]]=None
    intent:Optional[Literal["question","complaint","request","feedback","other"]]=None
    relevance:Optional[Literal["relevant","irrelevant"]]=None
    text_quality:Optional[Literal["clear","unclear"]]=None
    a_accuracy:Optional[int]=Field(None,ge=1,le=5); a_relevance:Optional[int]=Field(None,ge=1,le=5); a_clarity:Optional[int]=Field(None,ge=1,le=5); a_instruction_following:Optional[int]=Field(None,ge=1,le=5)
    b_accuracy:Optional[int]=Field(None,ge=1,le=5); b_relevance:Optional[int]=Field(None,ge=1,le=5); b_clarity:Optional[int]=Field(None,ge=1,le=5); b_instruction_following:Optional[int]=Field(None,ge=1,le=5)
    preferred_response:Optional[Literal["A","B","tie","both_bad"]]=None
    error_category:Optional[Literal["none","factual_error","hallucination","irrelevant","instruction_following","unsafe","poor_clarity","other"]]=None
    rationale:Optional[str]=Field(None,max_length=5000); reviewer_note:Optional[str]=Field(None,max_length=3000)
    status:Optional[Literal["pending","in_review","completed"]]=None
