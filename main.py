import argparse
import logging.config
import os
from logging.handlers import TimedRotatingFileHandler

from bot.Bot import AlarmCallBot
from configs import Config


def parse_args():
    parser = argparse.ArgumentParser(prog="Alarm Call Telegram Bot")
    parser.add_argument("--env", type=str, default="testing", choices=["testing", "production"], help="Environment to run bot")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.env == "testing":
        config = Config.TestConfig()
    else:
        config = Config.ProdConfig()

    # Setup logging
    os.makedirs(config.LOG_FILE_PATH, exist_ok=True)
    rotating_file_handler = TimedRotatingFileHandler(
        f"{config.LOG_FILE_PATH}/{config.LOG_FILE_NAME}",
        when="midnight",
        backupCount=30
    )
    rotating_file_handler.setLevel(logging.INFO)
    logging_handlers = []
    if config.DEBUG:
        logging_handlers.append(logging.StreamHandler())
    logging_handlers.append(rotating_file_handler)

    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=logging_handlers
    )

    logger = logging.getLogger(__name__)

    logger.info(f"Starting bot with environment = {args.env}")
    bot = AlarmCallBot(config=config)
    try:
        bot.start_polling()
    except Exception as exc:
        print(f"Unknown exception: {exc}")
    logger.info("Start polling...")
    bot.start_polling()

