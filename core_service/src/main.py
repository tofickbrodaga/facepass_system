from fastapi import FastAPI
from src.presentation.api.routes import router

app = FastAPI(
    title="FacePass Core Service",
    description="Microservice for Access Control Logic",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}