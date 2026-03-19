from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- 1. General App Config ---
    APP_NAME: str = "VPP Backend"
    ENV: str = "dev"
    API_V1_STR: str = "/api/v1"
    # --- 2. Database Config (Docker) ---
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # --- 3. Database Connection String ---
    DATABASE_URL: str

    # --- 4. Security ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # --- 5. Cloudinary Configuration ---
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # We use case_sensitive=True so Pydantic looks for exactly "DATABASE_URL" in the .env
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()