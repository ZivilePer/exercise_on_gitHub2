import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: snapshot original state
    original = copy.deepcopy(app_module.activities)
    yield
    # Assert: restore state after test
    app_module.activities = original

@pytest.fixture
def client():
    # Arrange: create a TestClient
    return TestClient(app_module.app)
