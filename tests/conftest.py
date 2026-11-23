# Each test gets its own empty database in a temporary folder.

import os
import sys

import pytest

os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-tests"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")

    # Load the app again so it picks up this test's database
    for name in [n for n in sys.modules if n == "app" or n.startswith("app.")]:
        del sys.modules[name]

    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def signed_in(client):
    client.post("/api/auth/register", json={
        "name": "Test User", "email": "test@example.com", "password": "password123",
    })
    return client
