def test_api_needs_sign_in(client):
    for url in ["/api/status", "/api/readings", "/api/reading", "/api/settings", "/api/auth/me"]:
        assert client.get(url).status_code == 401


def test_pages_send_signed_out_users_to_sign_in(client):
    for url in ["/", "/history", "/settings"]:
        response = client.get(url, follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/login"


def test_register_signs_the_user_in(client):
    response = client.post("/api/auth/register", json={
        "name": "Ada", "email": "ada@example.com", "password": "password123",
    })
    assert response.status_code == 201
    assert client.get("/api/auth/me").json() == {"name": "Ada", "email": "ada@example.com"}


def test_same_email_can_not_register_twice(signed_in):
    response = signed_in.post("/api/auth/register", json={
        "name": "Again", "email": "TEST@example.com", "password": "password123",
    })
    assert response.status_code == 409


def test_short_password_is_refused(client):
    response = client.post("/api/auth/register", json={
        "name": "Ada", "email": "ada@example.com", "password": "short",
    })
    assert response.status_code == 422


def test_password_is_stored_as_a_hash(signed_in):
    from app.database import SessionLocal
    from app.models import User

    with SessionLocal() as db:
        user = db.query(User).one()
    assert "password123" not in user.password_hash
    assert user.password_hash.startswith("$argon2")


def test_sign_out_then_sign_in(signed_in):
    assert signed_in.post("/api/auth/logout").status_code == 200
    assert signed_in.get("/api/status").status_code == 401

    response = signed_in.post("/api/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert signed_in.get("/api/status").status_code == 200


def test_wrong_password_and_unknown_email_give_the_same_answer(signed_in):
    signed_in.post("/api/auth/logout")
    wrong = signed_in.post("/api/auth/login", json={"email": "test@example.com", "password": "wrong-password"})
    unknown = signed_in.post("/api/auth/login", json={"email": "nobody@example.com", "password": "password123"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()
