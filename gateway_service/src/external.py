import httpx
from fastapi import HTTPException
from src.config import settings

class TevianClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.TEVIAN_TOKEN}"
        }

    async def search_face(self, image_bytes: bytes):
        """
        Отправляет фото в Tevian Search.
        Возвращает: face_id (str), liveness (float)
        """
        async with httpx.AsyncClient() as client:
            try:
                files = {'image': ('image.jpg', image_bytes, 'image/jpeg')}
                params = {
                    "gallery_name": "employees",
                    "liveness": "true",
                    "limit": 1
                }
                
                response = await client.post(
                    f"{settings.TEVIAN_API_URL}/search",
                    headers=self.headers,
                    files=files,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    print(f"Tevian Error: {response.text}")
                    raise HTTPException(status_code=502, detail="External Biometric API error")

                data = response.json()

                results = data.get('data', [])
                if not results:
                    raise HTTPException(status_code=404, detail="Face not found in database")

                match = results[0]
                face = match.get('face', {})

                liveness_data = face.get('liveness', {}).get('data', 0.0)
                
                return str(face['id']), float(liveness_data)

            except httpx.RequestError as e:
                print(f"Connection error: {e}")
                raise HTTPException(status_code=503, detail="Biometric service unavailable")