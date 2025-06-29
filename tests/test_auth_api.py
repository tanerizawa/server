from app.models.user import User


def test_register_creates_user(client):
    client_app, session_local = client
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret",
    }
    response = client_app.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data

    db = session_local()
    try:
        user = db.query(User).filter_by(email="alice@example.com").first()
        assert user is not None
    finally:
        db.close()


def test_login_returns_token(client):
    client_app, _ = client
    reg_payload = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "secret",
    }
    client_app.post("/api/v1/auth/register", json=reg_payload)

    response = client_app.post(
        "/api/v1/auth/login",
        json={"email": "bob@example.com", "password": "secret"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    client_app, _ = client
    reg_payload = {
        "username": "charlie",
        "email": "charlie@example.com",
        "password": "secret",
    }
    client_app.post("/api/v1/auth/register", json=reg_payload)

    response = client_app.post(
        "/api/v1/auth/login",
        json={"email": "charlie@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

