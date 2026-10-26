from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base
def now(): return datetime.utcnow()
class Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)
    prompt=Column(Text,nullable=False); text=Column(Text,default="",nullable=False)
    response_a=Column(Text,default="",nullable=False); response_b=Column(Text,default="",nullable=False)
    source=Column(String(120),default="manual",nullable=False); status=Column(String(30),default="pending",nullable=False,index=True)
    sentiment=Column(String(30)); intent=Column(String(30)); relevance=Column(String(30)); text_quality=Column(String(30))
    a_accuracy=Column(Integer); a_relevance=Column(Integer); a_clarity=Column(Integer); a_instruction_following=Column(Integer)
    b_accuracy=Column(Integer); b_relevance=Column(Integer); b_clarity=Column(Integer); b_instruction_following=Column(Integer)
    preferred_response=Column(String(30)); error_category=Column(String(50)); rationale=Column(Text); reviewer_note=Column(Text)
    created_at=Column(DateTime,default=now,nullable=False); updated_at=Column(DateTime,default=now,onupdate=now,nullable=False)
