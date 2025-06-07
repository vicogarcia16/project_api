import os
import sys
import pytest_asyncio
from dotenv import load_dotenv
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

# Asegura que estamos usando el entorno de test antes de importar nada más
load_dotenv(dotenv_path=".env.test", override=True)

# Asegura que la app se puede importar correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.db.database import engine, Base, AsyncSessionLocal, get_db

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_database():
    """
    Borra y crea las tablas antes de correr los tests (una vez por sesión).
    """
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(bind=sync_conn))
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn))

@pytest_asyncio.fixture(scope="function")
async def override_get_db():
    """
    Sobrescribe la dependencia get_db para usar la base de datos de prueba.
    """
    async def _get_db():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.pop(get_db, None)

@pytest_asyncio.fixture
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP asíncrono para pruebas.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
