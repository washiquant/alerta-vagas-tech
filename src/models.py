from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.database import Base

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150), nullable=True)
    workplace_type = Column(String(50), nullable=True) # Remoto, Híbrido, Presencial
    apply_url = Column(String(500), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notified = Column(Boolean, default=False)