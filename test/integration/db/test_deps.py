import pytest
from sqlalchemy import text
from app.db.deps import get_uow
from app.db.uow import UnitOfWork

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_get_uow_returns_unit_of_work():
    async for uow in get_uow():
        assert isinstance(uow, UnitOfWork)
        assert uow.session is not None

        result = await uow.session.execute(text("SELECT 1"))
        value = result.scalar()

    assert value == 1