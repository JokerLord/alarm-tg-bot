"""Config module."""
import os
import typing as tp
from dataclasses import dataclass


@dataclass
class BaseConfig:
    """
    Base config data class.

    Attributes:
        ZVONOK_API_URI (str): URI of call request server.
        ZVONOK_API_TOKEN (str): Zvonok API public key.
        ZVONOK_CAMPAIGN_ID (str): Zvonok campaign ID.
        CHANNELS_WITH_ALERTS (set): IDs of Telegram channels, where new posts will raise alerts.
        LOG_FILE_NAME (str): Log filename.

    """

    ZVONOK_API_URI: str
    ZVONOK_API_TOKEN: tp.Optional[str] = os.getenv("ZVONOK_API_TOKEN")
    ZVONOK_CAMPAIGN_ID: str = "270119321"

    CHANNELS_WITH_ALERTS: set = {-1002194118218}
    LOG_FILE_NAME: str = "alarm_call_bot.log"


@dataclass
class ProdConfig(BaseConfig):
    """
    Config class for production environment.

    Attributes:
        ZVONOK_API_URI (str): Zvonok server URI.
        DEBUG (bool): If True, sends log information to stdout,
        LOG_FILE_PATH: Path to log file.

    """

    ZVONOK_API_URI: str = "https://zvonok.com"
    DEBUG: bool = False
    LOG_FILE_PATH: str = "logs/prod"


@dataclass
class TestConfig(BaseConfig):
    """
    Config class for testing environment.

    Attributes:
        ZVONOK_API_URI (str): Testing server URI.
        DEBUG (bool): If True, sends log information to stdout,
        LOG_FILE_PATH: Path to log file.

    """

    ZVONOK_API_URI: str = "http://127.0.0.1:8080"
    DEBUG: bool = True
    LOG_FILE_PATH: str = "logs/test"
