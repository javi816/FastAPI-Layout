from typing import AsyncGenerator
from .session import AsyncSessionLocal
from .uow import UnitOfWork

async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    yield UnitOfWork(AsyncSessionLocal)