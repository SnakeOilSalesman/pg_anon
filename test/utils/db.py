import asyncpg

from common import exception_handler


# TODO: exception_handler looks excessive
@exception_handler
async def drop_and_recreate_db(connection: asyncpg.Connection, db_name: str, db_owner: str) -> None:
    """Drop and recreate database with given name."""
    await connection.execute(
        f"""
        SELECT pg_terminate_backend(pid)
          FROM pg_stat_activity
         WHERE pid <> pg_backend_pid()
               AND datname = %1
        """,
        db_name,
    )

    print(f"""DROP DATABASE IF EXISTS {db_name} and CREATE DATABASE""")
    await connection.execute(f"""DROP DATABASE IF EXISTS {db_name}""")
    await connection.execute(
        """
        CREATE DATABASE %1
          WITH OWNER = %2
               ENCODING = 'UTF8'
               LC_COLLATE = 'en_US.UTF-8'
               LC_CTYPE = 'en_US.UTF-8'
               template = template0
        """,
        db_name,
        db_owner,
    )


@exception_handler
async def create_db_if_not_exists(
    connection: asyncpg.Connection,
    db_name: str,
    db_owner: str,
) -> None:
    """Create database with given name if it doesn't exist."""
    db_exists = await connection.fetch(
        """SELECT datname from pg_database WHERE datname = %1""", db_name
    )
    if len(db_exists) != 0:
        return

    await connection.execute(
        """
        CREATE DATABASE %1
          WITH OWNER = %2
               ENCODING = 'UTF8'
               LC_COLLATE = 'en_US.UTF-8'
               LC_CTYPE = 'en_US.UTF-8'
               template = template0
        """,
        db_name,
        db_owner,
    )
