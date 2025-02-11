import pytest
from fastapi.exceptions import HTTPException

from ..dependencies import validate_token


def test_read_users(client, admin_access_token):
    # without admin access token
    response = client.get("/users/")
    assert response.status_code == 401

    # with admin access token
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = client.get("/users/", headers=headers)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert isinstance(data, list)

    assert len(data) == 3

    for user in data:
        assert "firstname" in user
        assert "lastname" in user
        assert "email" in user
        assert "disabled" in user
        assert "hashed_password" not in user


def test_create_user(client):
    user_data = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "password": "Qwerty123@",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()

    assert data["firstname"] == user_data["firstname"]
    assert data["lastname"] == user_data["lastname"]
    assert data["email"] == user_data["email"]
    assert data["disabled"] == False
    assert "hashed_password" not in data

    response_duplicate = client.post("/users/", json=user_data)
    assert response_duplicate.status_code == 409
    assert response_duplicate.json()["detail"] == "Email is already registered"

    response_missing_fields = client.post("/users/", json={})
    assert response_missing_fields.status_code == 422


def test_read_current_user(client, user_access_token):
    response = client.get("/users/me")
    assert response.status_code == 401

    headers = {"Authorization": f"Bearer {user_access_token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert "firstname" in data
    assert "lastname" in data
    assert "email" in data
    assert "disabled" in data
    assert "hashed_password" not in data


def test_update_current_user(client, user_access_token):
    response = client.put("/users/me", json={"firstname": "UpdatedName"})
    assert response.status_code == 401

    headers = {"Authorization": f"Bearer {user_access_token}"}
    update_payload = {"firstname": "UpdatedName", "password": "NewSecurePass"}

    response = client.put("/users/me", json=update_payload, headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["firstname"] == "UpdatedName"

    assert "lastname" in data
    assert "email" in data
    assert "disabled" in data
    assert "hashed_password" not in data


def test_delete_current_user(client, user_access_token):
    response = client.delete("/users/me")
    assert response.status_code == 401

    headers = {"Authorization": f"Bearer {user_access_token}"}

    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 204

    response = client.get("/users/me", headers=headers)
    assert response.status_code == 404


def test_delete_user(client, admin_access_token):
    response = client.delete("/users/1")
    assert response.status_code == 401

    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = client.delete("/users/1", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully."}

    response = client.delete("/users/1", headers=headers)
    assert response.status_code == 404

    response = client.get("/users/", headers=headers)
    data = response.json()

    assert len(data) == 2


def test_login_user(client, token_type):
    data = {"username": "alice@example.com", "password": "password1233"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = client.post("/users/auth/login", data=data, headers=headers)

    assert response.status_code == 400
    assert response.json() == {"detail": "Check email or password"}

    data = {"username": "bob@example.com", "password": "password123"}
    response = client.post("/users/auth/login", data=data, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Check email or password"}

    data = {"username": "alice@example.com", "password": "password123"}
    response = client.post("/users/auth/login", data=data, headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert "user" in data
    assert "access_token" in data
    assert "refresh_token" in response.cookies

    user = data["user"]
    assert "email" in user
    assert user["email"] == "alice@example.com"
    assert "firstname" in user
    assert "lastname" in user
    assert "disabled" in user

    access_token = data["access_token"]
    refresh_token = response.cookies["refresh_token"]

    try:
        payload = validate_token(access_token, token_type.ACCESS)
        assert payload["sub"] == "1"  # our user id form data
    except HTTPException as exc:
        pytest.fail(f"Access token validation failed: {exc.detail}")

    try:
        payload = validate_token(refresh_token, token_type.REFRESH)
        assert payload["sub"] == "1"
    except HTTPException as exc:
        pytest.fail(f"Refresh token validation failed: {exc.detail}")


def test_logout_user(client):
    login_data = {"username": "alice@example.com", "password": "password123"}
    login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login_response = client.post(
        "/users/auth/login", data=login_data, headers=login_headers
    )

    assert login_response.status_code == 200
    assert "refresh_token" in login_response.cookies

    logout_response = client.post("/users/auth/logout")

    assert logout_response.status_code == 200
    assert logout_response.json() == {"detail": "Successfully logged out"}

    assert "refresh_token" not in logout_response.cookies


def test_refresh_user_access_token(client, token_type):
    login_data = {"username": "alice@example.com", "password": "password123"}
    login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login_response = client.post(
        "/users/auth/login", data=login_data, headers=login_headers
    )

    assert login_response.status_code == 200

    refresh_response = client.get("/users/auth/refresh")

    assert refresh_response.status_code == 200
    refreshed_data = refresh_response.json()

    assert "access_token" in refreshed_data
    assert "user" in refreshed_data

    try:
        payload = validate_token(refreshed_data["access_token"], token_type.ACCESS)
        assert payload["sub"] == "1"
    except HTTPException as exc:
        pytest.fail(f"Refresh token validation failed: {exc.detail}")
