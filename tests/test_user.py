import pytest

REGISTER_URL = "/api/v1/user/register/"
LOGIN_URL = "/api/v1/user/login/"
REFRESH_URL = "/api/v1/user/refresh-token/"

TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"

@pytest.mark.asyncio
async def test_register_user(async_client):
    response = await async_client.post(REGISTER_URL, json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })

    assert response.status_code == 200
    data = response.json()["data"]
    assert "token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == TEST_EMAIL

@pytest.mark.asyncio
async def test_login_user(async_client):
    response = await async_client.post(LOGIN_URL, json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })

    assert response.status_code == 200
    data = response.json()["data"]
    assert "token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == TEST_EMAIL

@pytest.mark.asyncio
async def test_refresh_token(async_client):
    # Primero hacemos login para obtener el refresh_token
    login_response = await async_client.post(LOGIN_URL, json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })

    assert login_response.status_code == 200
    refresh_token = login_response.json()["data"]["refresh_token"]

    # Luego lo usamos para obtener un nuevo access token
    refresh_response = await async_client.post(
        REFRESH_URL,
        params={"refresh_token": refresh_token}
    )

    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
