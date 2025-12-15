from fastapi import FastAPI
from src.app.core.settings import settings

app = FastAPI(
    title= settings.APP_NAME,
    description= "AI system for automated literature review and hypothesis generation",
    version= "0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.APP_ENV, "app": settings.APP_NAME}
