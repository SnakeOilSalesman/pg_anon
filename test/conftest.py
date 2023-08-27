import os

import asyncpg
import pytest
import pytest_asyncio

from test import SQL_SCRIPTS_PATH
from test.entities import CommonValues, DatabaseCredentials
from test.utils.db import drop_and_recreate_db

SCALE_PLACEHOLDER: str = ':SCALE'
SCALE_DEFAULT_VALUE: int = 1512


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


@pytest_asyncio.fixture
def create_dbs(initial_db: asyncpg.Connection, common_values: CommonValues) -> None:
    """Create test databases intended for regular testing."""
    db_names = (
        common_values.SOURCE_DB,
        common_values.TARGET_DB,
        *[f'{common_values.TARGET_DB}_{n}' for n in range(2, 7)],
    )
    for name in db_names:
        drop_and_recreate_db(initial_db, name, common_values.DB_OWNER)

    yield

    # TODO: should we drop those tables here?


@pytest.fixture
def regular_env_init_script() -> str:
    """SQL script that creates and populates test tables for regular testing."""
    script_path = os.path.join(SQL_SCRIPTS_PATH, 'init_env_scalable.sql')
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()

    if script_text.find(str(SCALE_PLACEHOLDER)) < 1:
        pytest.exit(
            f'Invalid content of stress environment init script. '
            f'Scalable value placeholder ({SCALE_PLACEHOLDER}) not found in SQL script.\n'
            f'Consider checking the script content: {script_path}'
        )

    return script_text


@pytest.fixture
def stress_env_init_script() -> str:
    """SQL script that creates and populates test tables intended for stress testing."""
    script_path = os.path.join(SQL_SCRIPTS_PATH, 'init_stress_env.sql')
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()

    if script_text.find(str(SCALE_DEFAULT_VALUE)) < 1:
        pytest.exit(
            f'Invalid content of stress environment init script. '
            f'Scalable value ({SCALE_DEFAULT_VALUE}) not found in SQL script.\n'
            f'Consider checking the script content: {script_path}'
        )

    return script_text


@pytest_asyncio.fixture
async def set_test_env(
    create_dbs: None,
    source_db: asyncpg.Connection,
    regular_env_init_script: str,
    common_values: CommonValues,
) -> None:
    """Create regular test environment, create relations and insert test values."""
    await source_db.execute(
        regular_env_init_script.replace(
            SCALE_PLACEHOLDER, str(SCALE_DEFAULT_VALUE * common_values.SCALE)
        )
    )
    # TODO: should we drop everything created by "init_env" script? Or owned by test user?


@pytest_asyncio.fixture
async def set_stress_env(
    create_dbs: None,
    source_db: asyncpg.Connection,
    stress_env_init_script: str,
    common_values: CommonValues,
) -> None:
    """Create stress test environment, create relations and insert test values."""
    await source_db.execute(
        stress_env_init_script.replace(
            str(SCALE_DEFAULT_VALUE), str(SCALE_DEFAULT_VALUE * common_values.SCALE)
        )
    )
    # TODO: should we drop everything created by "init_env" script? Or owned by test user?
