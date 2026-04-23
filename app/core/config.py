from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    #app
    app_name: str = "FastAPI"
    debug: bool = False
    
    #database
    database_url: str = Field(..., alias="DATABASE_URL")
    database_url_async : str = Field(..., alias="DATABASE_URL_ASYNC")
    
    #tokens
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()