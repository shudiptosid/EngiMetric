from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional
from auth import get_current_user
from services.analytics_engine import (
    compute_complexity_score,
    estimate_hours,
    calculate_risk,
    acceptance_probability,
    predict_price,
    monte_carlo_simulation,
    optimize_profit,
    complexity_radar,
    full_analysis,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


# ─── Request Models ─────────────────────────────────────────────────

class ComplexityScoreRequest(BaseModel):
    hardware: int = Field(1, ge=0, le=5)
    software: int = Field(1, ge=0, le=5)
    ai_ml: int = Field(0, ge=0, le=5)
    deployment: int = Field(1, ge=0, le=5)
    risk_safety: int = Field(1, ge=0, le=5)


class AcceptanceRequest(BaseModel):
    quoted_price: float = Field(ge=0)
    predicted_optimal_price: float = Field(ge=0)
    classification: str = "Normal"
    client_type: str = "startup"
    risk_percent: float = Field(8.0, ge=0)


class PredictPriceRequest(BaseModel):
    estimated_hours: float = Field(120, ge=1)
    hourly_rate: float = Field(2500, ge=0)
    hardware_cost: float = Field(0, ge=0)
    risk_percent: float = Field(8.0, ge=0)
    profit_percent: float = Field(20.0, ge=0)
    total_score: int = Field(5, ge=0, le=25)
    classification: str = "Normal"


class MonteCarloRequest(BaseModel):
    base_hours: float = Field(120, ge=1)
    hourly_rate: float = Field(2500, ge=0)
    hardware_cost: float = Field(0, ge=0)
    risk_percent: float = Field(8.0, ge=0)
    has_ai: bool = False
    custom_pcb: bool = False
    rework_probability: float = Field(0.15, ge=0, le=1)
    delay_cost_per_week: float = Field(5000, ge=0)
    num_simulations: int = Field(5000, ge=100, le=50000)


class ProfitOptRequest(BaseModel):
    base_cost: float = Field(ge=0)
    classification: str = "Normal"
    client_type: str = "startup"
    risk_percent: float = Field(8.0, ge=0)


class RiskRequest(BaseModel):
    safety_critical: bool = False
    has_ai: bool = False
    custom_pcb: bool = False
    large_scale: bool = False


class FullAnalysisRequest(BaseModel):
    description: str = ""
    # 5 complexity dimensions (0-5 each)
    hardware_score: int = Field(1, ge=0, le=5)
    software_score: int = Field(1, ge=0, le=5)
    ai_ml_score: int = Field(0, ge=0, le=5)
    deployment_score: int = Field(1, ge=0, le=5)
    risk_safety_score: int = Field(1, ge=0, le=5)
    # Pricing
    hourly_rate: float = Field(0, ge=0)  # 0 = auto-detect from market
    hardware_cost: float = Field(0, ge=0)
    profit_percent: float = Field(20.0, ge=0)
    # Context
    client_type: str = "startup"
    safety_critical: bool = False
    has_ai: bool = False
    custom_pcb: bool = False
    large_scale: bool = False
    # Optional override
    quoted_price: Optional[float] = None


# ─── Endpoints ───────────────────────────────────────────────────────

@router.post("/complexity-score")
async def api_complexity_score(req: ComplexityScoreRequest, user=Depends(get_current_user)):
    return compute_complexity_score(req.hardware, req.software, req.ai_ml, req.deployment, req.risk_safety)


@router.post("/acceptance")
async def api_acceptance(req: AcceptanceRequest, user=Depends(get_current_user)):
    return acceptance_probability(
        req.quoted_price, req.predicted_optimal_price,
        req.classification, req.client_type, req.risk_percent,
    )


@router.post("/predict-price")
async def api_predict_price(req: PredictPriceRequest, user=Depends(get_current_user)):
    return predict_price(
        req.estimated_hours, req.hourly_rate, req.hardware_cost,
        req.risk_percent, req.profit_percent,
        req.total_score, req.classification,
    )


@router.post("/monte-carlo")
async def api_monte_carlo(req: MonteCarloRequest, user=Depends(get_current_user)):
    return monte_carlo_simulation(
        req.base_hours, req.hourly_rate, req.hardware_cost,
        req.risk_percent, req.has_ai, req.custom_pcb,
        req.rework_probability, req.delay_cost_per_week, req.num_simulations,
    )


@router.post("/profit-optimization")
async def api_profit_opt(req: ProfitOptRequest, user=Depends(get_current_user)):
    return optimize_profit(req.base_cost, req.classification, req.client_type, req.risk_percent)


@router.post("/risk")
async def api_risk(req: RiskRequest, user=Depends(get_current_user)):
    return calculate_risk(req.safety_critical, req.has_ai, req.custom_pcb, req.large_scale)


@router.post("/complexity-radar")
async def api_complexity_radar(req: ComplexityScoreRequest, user=Depends(get_current_user)):
    scores = {
        "hardware": req.hardware, "software": req.software, "ai_ml": req.ai_ml,
        "deployment": req.deployment, "risk_safety": req.risk_safety,
    }
    return complexity_radar(scores)


@router.post("/full")
async def api_full_analysis(req: FullAnalysisRequest, user=Depends(get_current_user)):
    return full_analysis(
        description=req.description,
        hardware_score=req.hardware_score,
        software_score=req.software_score,
        ai_ml_score=req.ai_ml_score,
        deployment_score=req.deployment_score,
        risk_safety_score=req.risk_safety_score,
        hourly_rate=req.hourly_rate,
        hardware_cost=req.hardware_cost,
        profit_percent=req.profit_percent,
        client_type=req.client_type,
        safety_critical=req.safety_critical,
        has_ai=req.has_ai,
        custom_pcb=req.custom_pcb,
        large_scale=req.large_scale,
        quoted_price=req.quoted_price,
    )
