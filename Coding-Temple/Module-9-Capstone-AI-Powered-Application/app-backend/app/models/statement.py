from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Statement(Base):
    __tablename__ = "statement"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # "pdf" or "csv"
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    
    # REMOVED transaction_type (or make nullable=True if you need backward compatibility)
    # transaction_type = Column(String, nullable=True)
    
    # Foreign Key connecting to Users
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Optional ChromaDB reference ID if you store the raw text embedding in ChromaDB
    chromadb_id = Column(String, nullable=True)

    # Relationship back to User
    user = relationship("User", back_populates="statements")