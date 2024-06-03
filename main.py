import argparse

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

    bot = AlarmCallBot(config=config)
    bot.start_polling()
