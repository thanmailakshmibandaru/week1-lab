from pathlib import Path
import importlib.util
import copy
import pytest
from fastapi.testclient import TestClient

# Load the application module from src/app.py so tests can import it regardless
# of whether src is a package.
ROOT = Path(__file__).resolve().parent.parent
APP_PATH = ROOT / "src" / "app.py"
spec = importlib.util.spec_from_file_location("app_module", str(APP_PATH))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)


@pytest.fixture
def appmod():
    """Provides the imported application module for tests."""
    return app_module


@pytest.fixture
def client():
    """Yields a TestClient and resets the in-memory activities state after each test.

    Arrange: make a deep copy of `activities`.
    Act: yield a TestClient bound to `app`.
    Assert/Teardown: restore the original activities state.
    """
    original = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    try:
        yield client
    finally:
        # restore activities to original state
        app_module.activities.clear()
        app_module.activities.update(original)
