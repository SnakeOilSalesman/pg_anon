import os

import asyncpg
import pytest
import pytest_asyncio

from test import SQL_SCRIPTS_PATH
from test.entities import CommonValues, DatabaseCredentials

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
