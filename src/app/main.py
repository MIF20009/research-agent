from fastapi import FastAPI
from src.app.core.settings import settings
from src.app.api.routes.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI system for automated literature review and hypothesis generation",
    version="0.1.0",
)

app.include_router(health_router)
