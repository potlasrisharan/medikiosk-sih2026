from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["Sarvam AI"])

class TTSRequest(BaseModel):
    text: str
    language_code: str = "te-IN"

class TTSResponse(BaseModel):
    audio_base64: Optional[str] = None
    language_code: str
    engine: str = "Sarvam Bulbul v2"

@router.post("/tts", response_model=TTSResponse)
async def get_sarvam_tts(req: TTSRequest):
    audio = await ai_service.generate_speech(req.text, req.language_code)
    return TTSResponse(audio_base64=audio, language_code=req.language_code)
