import os
import logging
import db
import typing as tp

from datetime import datetime, timedelta

import telebot
from telebot import types

import db
from bot import Messages, Utils
from configs import Config
from zvonok_api.Api import ZvonokManager

logger = logging.getLogger(__name__)


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        logger.error(f"Unknown exception: {exception}")
        return True


class AlarmCallBot:
    def __init__(self, config: tp.Union[Config.TestConfig, Config.ProdConfig]) -> None:
        self.__config = config
        self.__zvonok_manager = ZvonokManager(
            public_api_key=config.ZVONOK_API_TOKEN,
            campaign_id=config.ZVONOK_CAMPAIGN_ID,
            api_host=config.ZVONOK_API_URI,
            debug=config.DEBUG,
        )

        TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        if TELEGRAM_API_TOKEN is None:
            raise RuntimeError("Set TELEGRAM_API_TOKEN env. variable")

        self.__bot = telebot.TeleBot(
            TELEGRAM_API_TOKEN, exception_handler=ExceptionHandler
        )

        @self.__bot.message_handler(commands=["start"])
        def __start(message: telebot.types.Message, res=False):
            if not self.__check_private_chat(message):
                return
            logger.info(f"Start message from user with id = {message.from_user.id}")
            self.__bot.send_message(
                message.chat.id, Messages.START_MESSAGE, parse_mode="Markdown"
            )

        @self.__bot.message_handler(commands=["call"])
        def call(message: telebot.types.Message):
            if not self.__check_private_chat(message):
                return
            logger.info(f"Call message from user with id = {message.from_user.id}")
            if db.get_phone(message.from_user.id) is None:
                logger.info(
                    f"No number saved for user with id = {message.from_user.id}"
                )
                self.__bot.send_message(
                    message.chat.id,
                    Messages.NO_NUMBER_SAVED_MESSAGE,
                    parse_mode="Markdown",
                )
            else:
                try:
                    hours = Utils.parse_hours(message.text)
                    logger.info(
                        f"User with id = {message.from_user.id} add call for {hours} hours"
                    )
                except Exception as e:
                    logger.warning(f"Can't parse hours from message = {message.text}")
                    self.__bot.send_message(
                        message.chat.id, f"Ошибка в команде: {str(e)}"
                    )
                    return

                date_created = datetime.now()
                date_expired = date_created + timedelta(hours=hours)
                logger.info(
                    f"Creating call for user with id = {message.from_user.id} until {date_expired.strftime('%m/%d/%Y, %H:%M')}"
                )
                db.add_call(message.from_user.id, date_created, date_expired)
                self.__bot.send_message(
                    message.chat.id,
                    "Поставлен дозвон до " + date_expired.strftime("%m/%d/%Y, %H:%M"),
                )

        @self.__bot.channel_post_handler(content_types=["text"])
        def new_channel_post(message: telebot.types.Message):
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
        def set_phone(message: telebot.types.Message):
            if not self.__check_private_chat(message):
                return
            if db.get_phone(message.from_user.id) is None:
                logger.info(f"Get number from user with id = {message.from_user.id}")
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(
                    text="Отправить телефон", request_contact=True
                )
                keyboard.add(button_phone)
                self.__bot.send_message(
                    message.chat.id,
                    "Отправьте свой номер телефона нажав на кнопку",
                    reply_markup=keyboard,
                )
            else:
                logger.info(
                    f"Number from user with id = {message.from_user.id} already saved"
                )
                self.__bot.send_message(
                    message.chat.id, "Ваш номер уже сохранен в базе данных"
                )

        @self.__bot.message_handler(content_types=["contact"])
        def contact(message: telebot.types.Message):
            logger.info(
                f"Message with contact from user with id = {message.from_user.id}"
            )
            if message.contact is not None:
                db.add_phone(message.from_user.id, message.contact.phone_number)

    def start_polling(self):
        self.__bot.polling(none_stop=True, interval=0)

    def __check_private_chat(self, message: telebot.types.Message) -> bool:
        if message.chat.type != "private":
            logger.debug(
                f"Message /number was sent in public chat from user with id = {message.from_user.id}"
            )
            self.__bot.send_message(
                message.chat.id,
                "Для добавления номера напишите команду /number в личные сообщения боту",
            )
            return False
        return True
