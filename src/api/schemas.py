"""Typed inputs with bounded text, top-K and explicit analysis date."""
from datetime import date
from pydantic import BaseModel,Field
class ComplaintInput(BaseModel):
    text:str=Field(min_length=10,max_length=20000)
    device_name:str=Field(default='Infusion pump',max_length=200)
    manufacturer:str=Field(default='',max_length=200)
    model:str=Field(default='',max_length=200)
    serial_number:str=Field(default='',max_length=100)
    lot_number:str=Field(default='',max_length=100)
    patient_impact:str=Field(default='',max_length=1000)
    complaint_date:date=Field(default_factory=date.today)
    analysis_date:date=Field(default_factory=date.today)
    source:str=Field(default='user_entered',max_length=100)
    top_k:int=Field(default=5,ge=1,le=50)
class RegulatoryQuery(BaseModel):
    question:str=Field(min_length=5,max_length=4000)
    analysis_date:date=Field(default_factory=date.today)
class ReviewInput(BaseModel):
    reviewer:str=Field(min_length=1,max_length=200)
    notes:str=Field(min_length=1,max_length=10000)
