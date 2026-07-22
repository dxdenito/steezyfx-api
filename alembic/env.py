import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# --- Your app imports ---
from app.core.config import settings
from app.core.database import Base
from app.models.user import User  # noqa: F401 -- registers User with Base.metadata
from app.models import category  # noqa: F401 -- registers Category with Base.metadata
from app.models import post  # noqa: F401 -- registers Post with Base.metadata
from app.models import tag  # noqa: F401 -- registers Tag with Base.metadata
from app.models import (
    trade_execution,
)  # noqa: F401 -- registers Trade_execution with Base.metadata
from app.models import (
    trade_idea,
)  # noqa: F401 -- registers trade_idea with Base.metadata
from app.models import profile  # noqa: F401 -- registers profile with Base.metadata
from app.models.course import (
    Course,
)  # noqa: F401 -- registers course with Base.metadata
from app.models.enrollment import (
    Enrollment,
)  # noqa: F401 -- registers enrollment with Base.metadata
from app.models.lesson_progress import (
    LessonProgress,
)  # noqa: F401 -- registers lesson progress with Base.metadata
from app.models.module import (
    Module,
)  # noqa: F401 -- registers module with Base.metadata
from app.models.lesson import (
    Lesson,
)  # noqa: F401 -- registers lesson with Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override the ini file's URL with our real one from settings.
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is what Alembic diffs your models against to autogenerate migrations.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode -- generates SQL without a live DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Create an async engine and run migrations through it."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode -- entry point Alembic actually calls."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
