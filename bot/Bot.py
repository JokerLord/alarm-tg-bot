"""Alarm call bot class module."""
import os
import logging
import db
import typing as tp

from datetime import datetime, timedelta

import telebot
from telebot import types

from configs import Config
from zvonok_api.Api import ZvonokManager
from bot.Utils import _, check_private_chat, parse_call_hours

logger = logging.getLogger(__name__)


class ExceptionHandler(telebot.ExceptionHandler):
    """Telegram bot exception handler."""

    def handle(self, exception: Exception) -> bool:
        """
        Log unknown exception into logger.

        Args:
            exception: Exception to handle.

        Returns:
            True value.
        """
        logger.error(f"Unknown exception: {exception}")
        return True


class AlarmCallBot:
    """
    Alarm call bot class.

    Args:
        config (TestConfig | Prod _(Config): Data class with config information.
    """

    def __init__(self, config: tp.Union[Config.TestConfig, Config.ProdConfig]) -> None:
        """Alarm call bot constructor."""
        self.__config = config
        self.__zvonok_manager = ZvonokManager(
            public_api_key=config.ZVONOK_API_TOKEN,
            campaign_id=config.ZVONOK_CAMPAIGN_ID,
            api_host=config.ZVONOK_API_URI,
        )

        TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        if TELEGRAM_API_TOKEN is None:
            raise RuntimeError("Set TELEGRAM_API_TOKEN env. variable")

        self.__bot = telebot.TeleBot(
            TELEGRAM_API_TOKEN, exception_handler=ExceptionHandler
        )

        @self.__bot.message_handler(commands=["start"])
        def start(message: telebot.types.Message) -> None:
            """Command /start handler.

            Args:
                message: Telegram user message.
            """
            if not check_private_chat(self.__bot, message):
                return
            logger.info(f"Start message from user with id = {message.from_user.id}")
            self.__bot.send_message(
                message.chat.id,
                _("To set the call for N hours when urgent search fee appears use */call N* command"),
                parse_mode="Markdown"
            )

        @self.__bot.message_handler(commands=["call"])
        def call(message: telebot.types.Message) -> None:
            """Command /call N handler.

            Args:
                message: Telegram user message.
            """
            if not check_private_chat(self.__bot, message):
                return
            logger.info(f"Call message from user with id = {message.from_user.id}")
            if db.get_phone(message.from_user.id) is None:
                logger.info(
                    f"No number saved for user with id = {message.from_user.id}"
                )
                self.__bot.send_message(
                    message.chat.id,
                    _("There is no information which phone to set call for."
                      "Send your phone number with the command */number* in bot private messages"),
                    parse_mode="Markdown",
                )
            else:
                try:
                    hours = parse_call_hours(message.text)
                    logger.info(
                        f"User with id = {message.from_user.id} add call for {hours} hours"
                    )
                except Exception as e:
                    logger.warning(f"Can't parse hours from message = {message.text}")
                    self.__bot.send_message(
                        message.chat.id, _("Error in command: {}").format(str(e))
                    )
                    return

                date_created = datetime.now()
                date_expired = date_created + timedelta(hours=hours)
                logger.info(
                    f"Creating call for user with id = {message.from_user.id}"
                    f"until {date_expired.strftime('%m/%d/%Y, %H:%M')}"
                )
                db.add_call(message.from_user.id, date_created, date_expired)
                self.__bot.send_message(
                    message.chat.id,
                    _("The call is set until ") + date_expired.strftime("%m/%d/%Y, %H:%M")
                )

        @self.__bot.channel_post_handler(content_types=["text"])
        def new_channel_post(message: telebot.types.Message) -> None:
            """Post handler in channels with alert.

            Args:
                message: Telegram user message.
            """
            if message.chat.id not in self.__config.CHANNELS_WITH_ALERTS:
                logger.info(
                    f"Bot found message in chat with id = {message.chat.id}, but it's not in alerts channels"
                )
                return
            phones_to_call = db.get_phones_to_call(datetime.now())
            logger.info(f"Setting calls for phones = ({','.join(phones_to_call)})")
            for phone in phones_to_call:
                self.__zvonok_manager.create_call(phone)

        @self.__bot.message_handler(commands=["number"])
        def set_phone(message: telebot.types.Message) -> None:
            """Command /number handler.

            Args:
                message: Telegram user message.
            """
            if not check_private_chat(self.__bot, message):
                return
            if db.get_phone(message.from_user.id) is None:
                logger.info(f"Get number from user with id = {message.from_user.id}")
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(
                    text=_("Send phone number"), request_contact=True
                )
                keyboard.add(button_phone)
                self.__bot.send_message(
                    message.chat.id,
                    _("Send your phone number by clicking the button"),
                    reply_markup=keyboard,
                )
            else:
                logger.info(
                    f"Number from user with id = {message.from_user.id} already saved"
                )
                self.__bot.send_message(
                    message.chat.id, _("Your phone number is already saved in the database")
                )

        @self.__bot.message_handler(content_types=["contact"])
        def contact(message: telebot.types.Message) -> None:
            """User contact handler.

            Args:
                message: Telegram user message.
            """
            logger.info(
                f"Message with contact from user with id = {message.from_user.id}"
            )
            if message.contact is not None:
                db.add_phone(message.from_user.id, message.contact.phone_number)
                self.__bot.send_message(message.chat.id, _("Phone number successfully added!"))

    def start_polling(self):
        """Start bot polling."""
        self.__bot.polling(none_stop=True, interval=0)
