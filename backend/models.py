import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base
import enum


class UserRole(str, enum.Enum):
    FREELANCER = "freelancer"
    AGENCY = "agency"


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    APPROVED = "approved"
    COMPLETED = "completed"


class PricingModelType(str, enum.Enum):
    HOURLY = "hourly"
    FIXED = "fixed"
    VALUE_BASED = "value_based"
    COMPLEXITY_MULTIPLIER = "complexity_multiplier"
    MODULAR = "modular"


class DocumentType(str, enum.Enum):
    DOC = "doc"
    SHEET = "sheet"


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default=UserRole.FREELANCER)
    default_hourly_rate = Column(Float, default=50.0)
    company_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    complexity_score = Column(Float, nullable=True)
    complexity_level = Column(String, nullable=True)
    pricing_model = Column(String, default=PricingModelType.HOURLY)
    estimated_hours = Column(Float, nullable=True)
    final_cost = Column(Float, nullable=True)
    status = Column(String, default=ProjectStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="projects")
    hardware_items = relationship("HardwareItem", back_populates="project", cascade="all, delete-orphan")
    pricing_models = relationship("PricingModel", back_populates="project", cascade="all, delete-orphan")
    quotations = relationship("Quotation", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project")
    analytics = relationship("ProjectAnalytics", back_populates="project", uselist=False, cascade="all, delete-orphan")


class PricingModel(Base):
    __tablename__ = "pricing_models"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    model_type = Column(String, nullable=False)
    parameters = Column(JSON, default={})
    calculated_cost = Column(Float, nullable=True)
    breakdown = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="pricing_models")


class HardwareItem(Base):
    __tablename__ = "hardware_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    unit_cost = Column(Float, default=0.0)

    project = relationship("Project", back_populates="hardware_items")


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(JSON, default={})
    total_cost = Column(Float, default=0.0)
    status = Column(String, default="draft")
    valid_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="quotations")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    title = Column(String, nullable=False, default="Untitled Document")
    doc_type = Column(String, default=DocumentType.DOC)
    content = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="documents")
    project = relationship("Project", back_populates="documents")


class ProjectAnalytics(Base):
    """Analytics table for ML model training - stores historical project metrics."""
    __tablename__ = "project_analytics"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, unique=True)
    complexity_score = Column(Float, nullable=True)
    estimated_hours = Column(Float, nullable=True)
    actual_hours = Column(Float, nullable=True)
    quoted_price = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    accepted = Column(Boolean, nullable=True)
    profit_margin = Column(Float, nullable=True)
    client_type = Column(String, nullable=True)  # student, startup, enterprise
    category = Column(String, nullable=True)  # iot, ai, pcb, web, firmware
    industry = Column(String, nullable=True)
    risk_percent = Column(Float, nullable=True)
    overrun_percent = Column(Float, nullable=True)
    model_used = Column(String, nullable=True)
    hardware_cost = Column(Float, default=0.0)
    is_safety_critical = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="analytics")
