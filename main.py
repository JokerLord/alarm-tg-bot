import argparse
import logging
import logging.config

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

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("log_file.log"),
            logging.StreamHandler()
        ]
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

