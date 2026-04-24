from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Importar modelos para migraciones de Alembic
from app.modules.user import model as user_models
from app.modules.auth import model as auth_models