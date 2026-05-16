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
    FIREBASE_CREDENTIALS_PATH: str
    BOOTSTRAP_ADMIN_EMAILS: str = ""
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()