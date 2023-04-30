 

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Добавляем текущую директорию в sys.path
sys.path.insert(0, os.path.abspath('.'))

from alembic import context
from web import models
from web.base import Base
from web.database import engine





# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


def main():
    # подгружаем конфигурацию
    config = get_config()

    # создаем объект alembic с конфигурацией
    # и добавляем в него функцию run_migrations_online()
    # для генерации миграций из models.py
    alembic_cfg = Config(config.config_file_name)
    alembic_cfg.set_main_option('script_location', 'alembic')
    alembic_cfg.attributes['configure_logger'] = False
    alembic_cfg.cmd_opts = argparse.Namespace()
    alembic_cfg.cmd_opts.config = config.config_file_name

    # генерируем миграции из models.py
    if alembic_cfg.cmd_opts.generate:
        from alembic import command
        from alembic.context import EnvironmentContext

        with EnvironmentContext(alembic_cfg, script_dir=alembic_cfg.get_template_directory(), fn=run_migrations_online):
            command.revision(alembic_cfg, message, autogenerate=True)

    # выполняем миграции
    else:
        command.upgrade(alembic_cfg, 'head')


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
