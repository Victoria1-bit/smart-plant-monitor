# Each test gets its own empty database in a temporary folder.

import sys

import pytest


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
