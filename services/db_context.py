import os
from pathlib import Path
from typing import Any, Dict, List

from aerich.utils import get_models_describe
from nonebot import get_plugin_config, logger
from pydantic import BaseModel
from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.connection import connections

from aerich import Aerich, Command, get_app_connection
from aerich.migrate import MIGRATE_TEMPLATE, Migrate
from tortoise.utils import generate_schema_for_client, get_schema_sql

MODELS: List[str] = ["aerich.models"]

SCRIPT_METHOD = []


class Config(BaseModel):
    database_url: str


class TimestampMixin():
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now_add=True)


class ModelBase(Model):
    """
    自动添加模块

    Args:
        Model_ (_type_): _description_
    """

    id = fields.IntField(pk=True, generated=True, auto_increment=True)

    class Meta:
        abstract = True


config = get_plugin_config(Config)


async def __auto_migrate(config, app="toolsbot", location="./migrations", safe=True):
    """
    校验是
    """
    Migrate.app = app
    await Migrate.init(config, app, location)
    dirname = Path(location, app)
    if not dirname.exists():
        dirname.mkdir(parents=True)
        connection = get_app_connection(config, app)
        await generate_schema_for_client(connection, safe)
        #
        schema = get_schema_sql(connection, safe)

        version = await Migrate.generate_version()
        await Aerich.create(
            version=version,
            app=app,
            content=get_models_describe(app),
        )
        version_file = Path(dirname, version)
        content = MIGRATE_TEMPLATE.format(upgrade_sql=schema, downgrade_sql="")
        with open(version_file, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        await Migrate.migrate("update")


async def __upgrade(tortoise_config, app="toolsbot", location="./migrations", run_in_transaction=True):
    command = Command(tortoise_config, app=app, location=location)
    migrated = await command.upgrade(run_in_transaction=run_in_transaction)
    if not migrated:
        logger.info("No upgrade items found")
    else:
        for version_file in migrated:
            logger.info(f"Success upgrade {version_file}")


async def init():
    models = os.listdir("models")
    for model in models:
        if model.endswith(".py") and model != "__init__.py":
            model_name = f"models.{os.path.splitext(model)[0]}"
            MODELS.append(model_name)
    logger.debug(MODELS)
    try:
        tortoise_config = {
            "connections": {"default": config.database_url},
            "apps": {
                "toolsbot": {
                    "models": MODELS,
                    "default_connection": "default",
                },
            },
        }
        await Tortoise.init(tortoise_config)
        await __auto_migrate(tortoise_config)
        await __upgrade(tortoise_config)
    except Exception as e:
        raise Exception(f"数据库连接错误.... {type(e)}: {e}")


async def disconnect():
    await connections.close_all()
