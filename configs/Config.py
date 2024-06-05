import os
from dataclasses import dataclass


@dataclass
class BaseConfig:
    ZVONOK_API_URI: str
    ZVONOK_API_TOKEN: str = os.getenv("ZVONOK_API_TOKEN")
    ZVONOK_CAMPAIGN_ID: str = "270119321"

    CHANNELS_WITH_ALERTS = {-1002194118218}
    LOG_FILE_NAME = "alarm_call_bot.log"


@dataclass
class ProdConfig(BaseConfig):
    ZVONOK_API_URI: str = "https://zvonok.com"
    DEBUG: bool = False
    LOG_FILE_PATH: str = "logs/prod"


@dataclass
class TestConfig(BaseConfig):
    ZVONOK_API_URI: str = "http://127.0.0.1:8080"
    DEBUG: bool = True
    LOG_FILE_PATH: str = "logs/test"
