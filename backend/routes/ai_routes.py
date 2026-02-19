from fastapi import APIRouter, Depends
from models import User
from schemas import ComplexityAnalysisRequest, ComplexityAnalysisResponse
from auth import get_current_user
from services.ai_service import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])


@router.post("/analyze-complexity", response_model=ComplexityAnalysisResponse)
async def analyze_complexity(
    data: ComplexityAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    result = await ai_service.analyze_complexity(
        project_description=data.project_description,
        has_hardware=data.has_hardware,
        has_ai_ml=data.has_ai_ml,
        has_cloud=data.has_cloud,
        is_realtime=data.is_realtime,
        is_safety_critical=data.is_safety_critical,
    )
    return ComplexityAnalysisResponse(**result)
