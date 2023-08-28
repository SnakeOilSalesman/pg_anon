from dataclasses import dataclass, field

from test.utils.entities import get_factory


@dataclass
class DatabaseCredentials:
    """Execution parameters."""

    USER: str = field(default_factory=get_factory(str, 'TEST_DB_USER', 'anon_test_user'))
    PASSWORD: str = field(default_factory=get_factory(str, 'TEST_DB_USER_PASSWORD', 'mYy5RexGsZ'))
    HOST: str = field(default_factory=get_factory(str, 'TEST_DB_HOST', '127.0.0.1'))
    PORT: str = field(default_factory=get_factory(str, 'TEST_DB_PORT', '5432'))


@dataclass
class CommonValues:
    """Common test time values."""

    DB_OWNER: str = field(default_factory=get_factory(str, 'TEST_DB_USER', 'anon_test_user'))
    INITIAL_DB: str = field(default_factory=get_factory(str, 'TEST_INITIAL_DB', 'postgres'))
    SOURCE_DB: str = field(default_factory=get_factory(str, 'TEST_SOURCE_DB', 'test_source_db'))
    TARGET_DB: str = field(default_factory=get_factory(str, 'TEST_TARGET_DB', 'test_target_db'))
    SCALE: int = field(default_factory=get_factory(int, 'TEST_SCALE', '10'))
    THREADS: int = field(default_factory=get_factory(int, 'TEST_THREADS', '4'))
