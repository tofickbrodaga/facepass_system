from fastapi import FastAPI, UploadFile, File, HTTPException, status
import httpx
from src.config import settings
from src.external import TevianClient

app = FastAPI(title="FacePass Gateway", version="1.0.0")
tevian_client = TevianClient()

@app.post("/gate/enter")
async def enter_gate(terminal_id: int, file: UploadFile = File(...)):
    image_bytes = await file.read()

    face_id, liveness = await tevian_client.search_face(image_bytes)

    if liveness < settings.LIVENESS_THRESHOLD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Spoofing detected. You seem fake."
        )

    async with httpx.AsyncClient() as client:
        core_payload = {
            "face_id": face_id,
            "terminal_id": terminal_id,
            "liveness_score": liveness
        }
        
        try:
            response = await client.post(
                f"{settings.CORE_SERVICE_URL}/check-access",
                json=core_payload
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Core Service unavailable")

    if response.status_code == 200:
        return response.json()
    else:
        return response.json()

@app.get("/health")
async def health():
    return {"status": "gateway_ok"}