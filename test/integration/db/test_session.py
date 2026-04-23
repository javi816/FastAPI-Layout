import pytest
from sqlalchemy import text

pytestmark = pytest.mark.integration

async def test_async_session(async_session):
        result = await async_session.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1