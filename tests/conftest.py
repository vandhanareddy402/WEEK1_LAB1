import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

# Save the original activities dict for resetting between tests
original_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory activities dict before each test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))

@pytest.fixture
def client():
    # Arrange: Provide a TestClient for FastAPI app
    return TestClient(app)
