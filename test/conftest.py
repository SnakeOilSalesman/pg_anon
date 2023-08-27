import asyncpg
import pytest
import pytest_asyncio

from test.entities import CommonValues, DatabaseCredentials


@pytest.fixture
def db_creds() -> DatabaseCredentials:
    """Database credentials."""
    return DatabaseCredentials()


@pytest.fixture
def common_values() -> CommonValues:
    """Common values used during testing."""
    return CommonValues()


@pytest_asyncio.fixture
async def initial_db(
    db_creds: DatabaseCredentials,
    common_values: CommonValues,
) -> asyncpg.Connection:
    """Root database connection required when no other DB instance exist."""
    connection = await asyncpg.connect(
        host=db_creds.HOST,
        port=db_creds.PORT,
        user=db_creds.USER,
        password=db_creds.PASSWORD,
        database=common_values.INITIAL_DB,
    )
    yield connection
    connection.close()


@pytest_asyncio.fixture
async def source_db(
    db_creds: DatabaseCredentials,
    common_values: CommonValues,
) -> asyncpg.Connection:
    """Source DB connection."""
    connection = await asyncpg.connect(
        host=db_creds.HOST,
        port=db_creds.PORT,
        user=db_creds.USER,
        password=db_creds.PASSWORD,
        database=common_values.SOURCE_DB,
    )
    yield connection
    connection.close()
