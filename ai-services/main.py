from fastapi import FastAPI
from endpoints import router

app = FastAPI(title="PIIS AI Service")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "PIIS AI Service is running"}