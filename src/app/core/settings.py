import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Multi-Agent Research Assistant")
    APP_ENV: str = os.getenv("APP_ENV", "local")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

settings = Settings()