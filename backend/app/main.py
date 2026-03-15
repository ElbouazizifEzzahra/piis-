# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="PIIS API",
    description="Proactive Infrastructure Intelligence System",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}