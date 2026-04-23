from app.core.config import settings
import pytest

pytestmark = pytest.mark.unit

def test_settings_loaded():
    assert settings.database_url is not None
    assert settings.database_url_async is not None
    assert settings.app_name is not None