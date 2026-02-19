from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr


# ─── Auth Schemas ───────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "freelancer"
    company_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    default_hourly_rate: float
    company_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdate(BaseModel):
    name: Optional[str] = None
    default_hourly_rate: Optional[float] = None
    company_name: Optional[str] = None


# ─── Project Schemas ───────────────────────────────────────
class ProjectCreate(BaseModel):
    client_name: str
    client_email: Optional[str] = None
    description: str
    pricing_model: str = "hourly"


class ProjectUpdate(BaseModel):
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    description: Optional[str] = None
    complexity_score: Optional[float] = None
    complexity_level: Optional[str] = None
    pricing_model: Optional[str] = None
    estimated_hours: Optional[float] = None
    final_cost: Optional[float] = None
    status: Optional[str] = None


class HardwareItemSchema(BaseModel):
    name: str
    quantity: int = 1
    unit_cost: float = 0.0


class ProjectResponse(BaseModel):
    id: str
    user_id: str
    client_name: str
    client_email: Optional[str] = None
    description: str
    complexity_score: Optional[float] = None
    complexity_level: Optional[str] = None
    pricing_model: str
    estimated_hours: Optional[float] = None
    final_cost: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ─── AI Complexity Schemas ─────────────────────────────────
class ComplexityAnalysisRequest(BaseModel):
    project_description: str
    has_hardware: bool = False
    has_ai_ml: bool = False
    has_cloud: bool = False
    is_realtime: bool = False
    is_safety_critical: bool = False


class ComplexityAnalysisResponse(BaseModel):
    complexity_score: float
    complexity_level: str
    pricing_multiplier: float
    suggested_hours_min: int
    suggested_hours_max: int
    risk_percentage: float
    rate_category: str
    ai_analysis: Optional[str] = None
    breakdown: Dict[str, float] = {}


# ─── Pricing Schemas ──────────────────────────────────────
class PricingCalculateRequest(BaseModel):
    model_type: str  # hourly, fixed, value_based, complexity_multiplier, modular
    hourly_rate: float = 50.0
    estimated_hours: float = 0.0
    risk_percentage: float = 10.0
    profit_margin: float = 15.0
    hardware_costs: float = 0.0
    software_costs: float = 0.0
    maintenance_months: int = 0
    maintenance_monthly_rate: float = 0.0
    complexity_multiplier: float = 1.0
    estimated_client_revenue: float = 0.0
    value_percentage: float = 10.0
    modules: Optional[Dict[str, float]] = None  # module_name: hours


class PricingCalculateResponse(BaseModel):
    model_type: str
    subtotal: float
    hardware_cost: float
    software_cost: float
    risk_amount: float
    profit_amount: float
    maintenance_cost: float
    total_cost: float
    breakdown: Dict[str, Any] = {}


# ─── Quotation Schemas ────────────────────────────────────
class QuotationCreate(BaseModel):
    project_id: str
    title: str
    content: Dict[str, Any] = {}
    total_cost: float = 0.0
    valid_until: Optional[datetime] = None


class QuotationUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    total_cost: Optional[float] = None
    status: Optional[str] = None
    valid_until: Optional[datetime] = None


class QuotationResponse(BaseModel):
    id: str
    project_id: str
    title: str
    content: Dict[str, Any]
    total_cost: float
    status: str
    valid_until: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Proposal Generation Schemas ──────────────────────────
class ProposalGenerateRequest(BaseModel):
    project_id: str
    project_name: str
    client_name: str
    project_description: str
    scope_items: List[str] = []
    timeline_weeks: int = 4
    total_cost: float = 0.0
    payment_terms: str = "50% upfront, 50% on delivery"
    include_maintenance: bool = True
    maintenance_monthly: float = 0.0


class ProposalGenerateResponse(BaseModel):
    title: str
    sections: Dict[str, str]
    generated_at: datetime


# ─── Document Schemas ─────────────────────────────────────
class DocumentCreate(BaseModel):
    title: str = "Untitled Document"
    doc_type: str = "doc"
    project_id: Optional[str] = None
    content: Dict[str, Any] = {}


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    project_id: Optional[str] = None
    title: str
    doc_type: str
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
