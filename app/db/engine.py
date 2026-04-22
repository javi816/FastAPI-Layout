from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.database_url_async,
    echo=True,
    pool_pre_ping=True
)
