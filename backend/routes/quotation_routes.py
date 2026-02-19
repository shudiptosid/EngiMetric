from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import get_db
from models import User, Quotation, Project
from schemas import (
    QuotationCreate, QuotationUpdate, QuotationResponse,
    ProposalGenerateRequest, ProposalGenerateResponse,
)
from auth import get_current_user
from services.export_service import export_service

router = APIRouter(prefix="/api/quotations", tags=["Quotations"])


@router.get("/", response_model=List[QuotationResponse])
async def list_quotations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Quotation)
        .join(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Quotation.created_at.desc())
    )
    quotations = result.scalars().all()
    return [QuotationResponse.model_validate(q) for q in quotations]


@router.post("/", response_model=QuotationResponse)
async def create_quotation(
    data: QuotationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify project ownership
    project = await db.execute(
        select(Project).where(Project.id == data.project_id, Project.user_id == current_user.id)
    )
    if not project.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    quotation = Quotation(
        project_id=data.project_id,
        title=data.title,
        content=data.content,
        total_cost=data.total_cost,
        valid_until=data.valid_until,
    )
    db.add(quotation)
    await db.flush()
    await db.refresh(quotation)
    return QuotationResponse.model_validate(quotation)


@router.get("/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(
    quotation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Quotation)
        .join(Project)
        .where(Quotation.id == quotation_id, Project.user_id == current_user.id)
    )
    quotation = result.scalar_one_or_none()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return QuotationResponse.model_validate(quotation)


@router.put("/{quotation_id}", response_model=QuotationResponse)
async def update_quotation(
    quotation_id: str,
    data: QuotationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Quotation)
        .join(Project)
        .where(Quotation.id == quotation_id, Project.user_id == current_user.id)
    )
    quotation = result.scalar_one_or_none()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(quotation, field, value)
    db.add(quotation)
    await db.flush()
    await db.refresh(quotation)
    return QuotationResponse.model_validate(quotation)


@router.get("/{quotation_id}/export")
async def export_quotation(
    quotation_id: str,
    format: str = "pdf",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Quotation)
        .join(Project)
        .where(Quotation.id == quotation_id, Project.user_id == current_user.id)
    )
    quotation = result.scalar_one_or_none()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    quotation_data = {
        "title": quotation.title,
        "content": quotation.content,
        "total_cost": quotation.total_cost,
        "status": quotation.status,
    }

    if format == "pdf":
        file_bytes = export_service.generate_pdf(quotation_data)
        return Response(
            content=file_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{quotation.title}.pdf"'},
        )
    elif format == "docx":
        file_bytes = export_service.generate_docx(quotation_data)
        return Response(
            content=file_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{quotation.title}.docx"'},
        )
    elif format == "xlsx":
        file_bytes = export_service.generate_xlsx(quotation_data)
        return Response(
            content=file_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{quotation.title}.xlsx"'},
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use pdf, docx, or xlsx.")


@router.post("/generate-proposal", response_model=ProposalGenerateResponse)
async def generate_proposal(
    data: ProposalGenerateRequest,
    current_user: User = Depends(get_current_user),
):
    """Auto-generate a complete project proposal."""
    sections = {
        "project_overview": (
            f"This proposal outlines the scope, timeline, and costs for the '{data.project_name}' project "
            f"for {data.client_name}. {data.project_description}"
        ),
        "scope_of_work": "\n".join(
            [f"• {item}" for item in data.scope_items]
            if data.scope_items
            else [
                "• Requirements analysis and technical specification",
                "• System architecture and design",
                "• Development and implementation",
                "• Testing and quality assurance",
                "• Documentation and knowledge transfer",
                "• Deployment and go-live support",
            ]
        ),
        "timeline": (
            f"The project is estimated to take approximately {data.timeline_weeks} weeks. "
            f"Milestones will be defined during the kickoff meeting with regular progress updates "
            f"provided throughout the development cycle."
        ),
        "cost_summary": f"Total Project Cost: ${data.total_cost:,.2f}",
        "payment_terms": data.payment_terms,
        "maintenance_plan": (
            f"Post-delivery maintenance and support available at ${data.maintenance_monthly:,.2f}/month. "
            f"Includes bug fixes, minor updates, and technical support during business hours."
        ) if data.include_maintenance else "Maintenance plan not included in this proposal.",
        "legal_disclaimer": (
            "This proposal is valid for 30 days from the date of issue. "
            "The final cost may vary based on scope changes agreed upon by both parties. "
            "All intellectual property developed during the project will be transferred to the client upon final payment. "
            "Confidentiality of all project-related information is guaranteed."
        ),
    }

    return ProposalGenerateResponse(
        title=f"Proposal: {data.project_name}",
        sections=sections,
        generated_at=datetime.utcnow(),
    )
