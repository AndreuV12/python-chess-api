import pytest
import httpx
from app.main import app


@pytest.fixture
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
async def setup_openings():
    # Configura los datos de prueba
    app.state.openings = [{"id": 1, "name": "Opening 1"}]
    yield
    # Limpia los datos después de la prueba
    app.state.openings = []


@pytest.mark.asyncio
async def test_read_user_openings(client: httpx.AsyncClient):
    res = await client.get("/openings")
    print(res)
    assert len(res.json()["openings"]) == 1
