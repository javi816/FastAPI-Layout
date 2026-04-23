import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://app_user:app_password@localhost:5432/app_db"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

async def main():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(result.scalar())

    await engine.dispose()

asyncio.run(main())
