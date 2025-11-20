from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TEVIAN_API_URL: str = "https://backend.facecloud.tevian.ru/api/v1"
    TEVIAN_EMAIL: str = "new-user@example.com" 
    TEVIAN_PASSWORD: str = "password"
    TEVIAN_TOKEN: str = ""
    CORE_SERVICE_URL: str = "http://core-service:8000/api/v1"

    LIVENESS_THRESHOLD: float = 0.8

    class Config:
        env_file = "../.env"
        extra = "ignore"

settings = Settings()