from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # PostgreSQL - supports full URL or individual components
    POSTGRES_URL: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None
    
    # MongoDB - supports full URL or individual components
    MONGO_URI: str
    MONGO_DB: str = "healthcare_ml"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Machine Learning Pipeline"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_postgres_url(self) -> str:
        """Get PostgreSQL connection URL, preferring POSTGRES_URL if provided."""
        if self.POSTGRES_URL:
            return self.POSTGRES_URL
        
        # Build URL from components if not provided as full URL
        if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB]):
            port = f":{self.POSTGRES_PORT}" if self.POSTGRES_PORT else ""
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}{port}/{self.POSTGRES_DB}"
        
        raise ValueError("PostgreSQL connection URL or components must be provided")


settings = Settings()
