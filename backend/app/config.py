from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/opensnap"
    
    # Redis/KeyDB
    REDIS_URL: str = "redis://localhost:6379"
    
    # Storage
    STORAGE_PROVIDER: str = "minio"  # or "s3"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "opensnap"
    
    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    # Moderation
    MODERATION_API_URL: str = "http://moderation-service:8001"
    HITL_DASHBOARD_URL: str = "http://localhost:3002"
    
    # Recommendations
    RECOMMENDATION_API_URL: str = "http://recommendation-service:8002"
    
    class Config:
        env_file = ".env"

settings = Settings()
