from app.models.user import User


def test_get_current_user(client):
    client_app, _ = client
    response = client_app.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "tester"
    assert data["email"] == "tester@example.com"
    assert data["id"] == 1


def test_delete_current_user(client):
    client_app, session_local = client
    resp = client_app.delete("/api/v1/users/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    db = session_local()
    try:
        assert db.query(User).filter_by(id=1).first() is None
    finally:
        db.close()

