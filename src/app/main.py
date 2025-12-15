from fastapi import FastAPI

app = FastAPI(
    title= "Multi agent research agent",
    description= "AI system for automated literature review and hypothesis generation",
    version= "0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
