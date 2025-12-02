from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="projects")
    recordings = relationship("Recording", back_populates="project")

class Recording(Base):
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    filename = Column(String(255))
    file_path = Column(String(500))
    duration = Column(Float)
    sample_rate = Column(Integer)
    channels = Column(Integer)
    format = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="recordings")
    effects = relationship("EffectLog", back_populates="recording")

class EffectLog(Base):
    __tablename__ = "effect_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("recordings.id"))
    effect_type = Column(String(50))
    parameters = Column(Text)
    applied_at = Column(DateTime, default=datetime.utcnow)
    
    recording = relationship("Recording", back_populates="effects")
