from pydantic import BaseModel
from loguru import logger
import ujson
import yaml
import os


class DB(BaseModel):
    db_name: str
    table_name: str = "contacts"


class Config(BaseModel):
    db: DB


def load_config(config_file: Config = None):
    if not config_file:
        config_file = os.getenv('CONFIG_FILE', '/home/helen/PycharmProjects/otus_hw/note_book/configs/config.yaml')
    with open(config_file, "r") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    logger.info('Config is loaded')
    return Config.model_validate_json(ujson.dumps(config))