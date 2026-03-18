from src.services.auth import AuthService
import pytest


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_token(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]


@pytest.mark.parametrize("email, password, status_code", [
    ("user1@gmail.com", "qwerty1", 200),
    ("user2@gmail.com", "qwerty2", 200),
    ("user3@gmail.com", "qwerty2", 200),
])
async def test_register_login_logout(
        email,
        password,
        status_code,
        ac):

        register_resp = await ac.post(
            "/auth/register",
            json={
                "email": email,
                "password": password
            }
        )
        assert register_resp.status_code == status_code

        login_resp = await ac.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        assert login_resp.status_code == status_code
        assert login_resp.json()["access_token"]

        check_user_resp = await ac.get(
            "/auth/me"
        )
        assert check_user_resp.status_code == status_code

        logout_resp = await ac.delete(
            "/auth/logout"
        )
        assert logout_resp.status_code == status_code

        check_user_resp = await ac.get(
            "/auth/me"
        )
        assert check_user_resp.status_code == 401