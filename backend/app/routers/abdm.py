from fastapi import APIRouter
from ..models.schemas import ABHAVerifyRequest, PatientProfile
from ..services.abdm_service import abdm_service

router = APIRouter(prefix="/abdm", tags=["ABDM"])

@router.post("/abha/verify", response_model=PatientProfile)
async def verify_abha(req: ABHAVerifyRequest):
    query = req.qr_payload or req.abha_number or "91-4829-1029-4821"
    return abdm_service.verify_abha(query)
