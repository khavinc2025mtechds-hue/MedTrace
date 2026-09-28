"""Normalized audit entities plus a complete reproducible investigation snapshot."""
from datetime import datetime,timezone
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Text,JSON,Float,ForeignKey
class Base(DeclarativeBase):pass
class Complaint(Base):
    __tablename__='complaints'
    id:Mapped[str]=mapped_column(String,primary_key=True)
    text:Mapped[str]=mapped_column(Text)
    fields:Mapped[dict]=mapped_column(JSON)
    created_at:Mapped[str]=mapped_column(String,default=lambda:datetime.now(timezone.utc).isoformat())
class Device(Base):
    __tablename__='devices'
    id:Mapped[int]=mapped_column(primary_key=True)
    complaint_id:Mapped[str]=mapped_column(ForeignKey('complaints.id'))
    details:Mapped[dict]=mapped_column(JSON)
class Investigation(Base):
    __tablename__='investigation_results'
    id:Mapped[str]=mapped_column(String,primary_key=True)
    complaint_id:Mapped[str]=mapped_column(ForeignKey('complaints.id'))
    result:Mapped[dict]=mapped_column(JSON)
    review_status:Mapped[str]=mapped_column(String,default='pending_human_review')
    reviewer:Mapped[str]=mapped_column(String,default='')
    review_notes:Mapped[str]=mapped_column(Text,default='')
class SimilarCase(Base):
    __tablename__='similar_cases'
    id:Mapped[int]=mapped_column(primary_key=True)
    investigation_id:Mapped[str]=mapped_column(ForeignKey('investigation_results.id'))
    report_key:Mapped[str]=mapped_column(String)
    score:Mapped[float]=mapped_column(Float)
class PriorityScore(Base):
    __tablename__='priority_scores'
    id:Mapped[int]=mapped_column(primary_key=True)
    investigation_id:Mapped[str]=mapped_column(ForeignKey('investigation_results.id'))
    details:Mapped[dict]=mapped_column(JSON)
class RegulatoryEvidence(Base):
    __tablename__='regulatory_evidence'
    id:Mapped[int]=mapped_column(primary_key=True)
    investigation_id:Mapped[str]=mapped_column(ForeignKey('investigation_results.id'))
    details:Mapped[dict]=mapped_column(JSON)
class Report(Base):
    __tablename__='reports'
    id:Mapped[int]=mapped_column(primary_key=True)
    investigation_id:Mapped[str]=mapped_column(ForeignKey('investigation_results.id'))
    markdown:Mapped[str]=mapped_column(Text)
