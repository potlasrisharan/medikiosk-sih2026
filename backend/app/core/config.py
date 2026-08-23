from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediKiosk Clinical Intelligence Gateway"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SARVAM_API_KEY: Optional[str] = "mock_sarvam_key"
    EKA_CLIENT_ID: Optional[str] = "mock_eka_client_id"
    EKA_CLIENT_SECRET: Optional[str] = "mock_eka_secret"
    
    RED_FLAG_TIMEOUT_MS: int = 150
    DEFAULT_HOSPITAL_NAME: str = "All India Institute of Ayurveda (AIIA)"
    DEFAULT_HOSPITAL_ID: str = "IN0110000142"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
