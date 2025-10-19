from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    DEBUG: bool = False
    
    # Email settings
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = None
    SMTP_PASSWORD: str = None
    EMAIL_FROM: str = None
    EMAIL_TO: str = None

settings = Settings()
