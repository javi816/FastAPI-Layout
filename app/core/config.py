from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    #app
    app_name: str = "FastAPI"
    debug: bool = False
    
    #database
    database_url: str = Field(..., alias="DATABASE_URL")
    database_url_async : str = Field(..., alias="DATABASE_URL_ASYNC")
    
    #auth
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_TOKEN_URL: str
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()