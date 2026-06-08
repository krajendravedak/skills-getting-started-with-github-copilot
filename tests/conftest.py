import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(scope="session")
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app_module.app)


# Capture the original activities state so tests can reset it
_original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the module-level `activities` dict before each test to ensure isolation."""
    app_module.activities = copy.deepcopy(_original_activities)
    yield
    app_module.activities = copy.deepcopy(_original_activities)
