from fastapi import APIRouter, Depends
from models import User
from schemas import PricingCalculateRequest, PricingCalculateResponse
from auth import get_current_user
from services.pricing_engine import pricing_engine

router = APIRouter(prefix="/api/pricing", tags=["Pricing"])


@router.post("/calculate", response_model=PricingCalculateResponse)
async def calculate_pricing(
    data: PricingCalculateRequest,
    current_user: User = Depends(get_current_user),
):
    result = pricing_engine.calculate(data.model_dump())
    return PricingCalculateResponse(**result)
