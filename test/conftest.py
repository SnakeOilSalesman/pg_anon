import pytest

from test.entities import CommonValues, DatabaseCredentials


@pytest.fixture
def db_creds() -> DatabaseCredentials:
    """Database credentials."""
    return DatabaseCredentials()


@pytest.fixture
def common_values() -> CommonValues:
    """Common values used during testing."""
    return CommonValues()
