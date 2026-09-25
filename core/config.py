import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin")
    
    SMTP_USERNAME: str | None = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")
    SMTP_HOST: str | None = os.getenv("SMTP_HOST")
    SMTP_PORT: str = os.getenv("SMTP_PORT", "465")
    CLINIC_EMAIL: str = os.getenv("CLINIC_EMAIL", "procare.vishva@gmail.com")

settings = Settings()
