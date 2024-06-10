"""Utility functions for Bot class."""
import re
import telebot
import logging
import locale
import gettext


logger = logging.getLogger(__name__)


LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation("bot", "po", ["ru_RU.UTF-8"], fallback=True),
    ("en_US", "UTF-8"): gettext.NullTranslations(),
}


def _(text: str) -> str:
    return LOCALES[locale.getlocale()].gettext(text)


def parse_call_hours(message: str) -> int:
    """
    Parse hours from /call message.

    Arguments:
        message: Telegram message in format '/call N'.

    Returns:
        hours: N in message, the number of hours during which bot can call the user.
    """
    matcher = re.match(r"/call[\s]*(\d+)", message)
    if matcher is None:
        # raise ValueError("Сообщение должно соответствовать шаблону /call hours")
        raise ValueError(_("The message must match the pattern /call hours"))
    hours = int(matcher.group(1))
    if not hours > 0:
        # raise ValueError("Количество часов должно быть больше 0")
        raise ValueError(_("Number of hours must be greater than 0"))

    return hours


def check_private_chat(bot: telebot.TeleBot, message: telebot.types.Message) -> bool:
    """Check if user sends message in bot private chat."""
    if message.chat.type != "private":
        logger.debug(
            f"Message /number was sent in public chat from user with id = {message.from_user.id}"
        )
        # bot.send_message(
        #     message.chat.id,
        #     "Для добавления номера напишите команду /number в личные сообщения боту",
        # )
        bot.send_message(
            message.chat.id,
            _("To add a phone number write the command /number in a private message to the bot"),
        )
        return False
    return True
