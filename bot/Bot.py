import os
import db
import typing as tp

from datetime import datetime, timedelta

import telebot
from telebot import types

import db
from bot import Messages, Utils
from configs import Config
from zvonok_api.Api import ZvonokManager


class AlarmCallBot:
    def __init__(self, config: tp.Union[Config.TestConfig, Config.ProdConfig]) -> None:
        self.__zvonok_manager = ZvonokManager(
            public_api_key=config.ZVONOK_API_TOKEN,
            campaign_id=config.ZVONOK_CAMPAIGN_ID,
            api_host=config.ZVONOK_API_URI,
            debug=config.DEBUG
        )

        TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        if TELEGRAM_API_TOKEN is None:
            raise RuntimeError("Set TELEGRAM_API_TOKEN env. variable")
        
        self.__bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

        @self.__bot.message_handler(commands=["start"])
        def __start(message: telebot.types.Message, res=False):
            self.__bot.send_message(message.chat.id, Messages.START_MESSAGE, parse_mode="Markdown")

        @self.__bot.message_handler(commands=["call"])
        def call(message: telebot.types.Message):
            if len(db.get_phone(message.from_user.id)) == 0:
                self.__bot.send_message(message.chat.id, Messages.NO_NUMBER_SAVED_MESSAGE, parse_mode="Markdown")
            else:
                try:
                    hours = Utils.parse_hours(message.text)
                except Exception as e:
                    self.__bot.send_message(message.chat.id, f"Ошибка в команде: {str(e)}")
                    return
                
                date_created = datetime.now()
                date_expired = date_created + timedelta(hours=hours)
                db.add_call(message.from_user.id, date_created, date_expired)
                self.__bot.send_message(message.chat.id, "Поставлен дозвон до " + date_expired.strftime("%m/%d/%Y, %H:%M"))

        @self.__bot.channel_post_handler(content_types=["text"])
        def new_channel_post(message: telebot.types.Message):
            phones_to_call = db.get_phones_to_call(datetime.now())
            for phone in phones_to_call:
                self.__zvonok_manager.create_call(phone)

        @self.__bot.message_handler(commands=["number"])
        def phone(message: telebot.types.Message):
            if message.chat.type != "private":
                self.__bot.send_message(
                    message.chat.id,
                    "Номер можно добавить только в личных сообщениях с ботом"
                )
                return 
            if len(db.get_phone(message.from_user.id)) == 0:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
                keyboard.add(button_phone)
                self.__bot.send_message(
                    message.chat.id,
                    "Отправьте свой номер телефона нажав на кнопку",
                    reply_markup=keyboard
                )
            else:
                self.__bot.send_message(message.chat.id, "Ваш номер уже сохранен в базе данных")

        @self.__bot.message_handler(content_types=["contact"])
        def contact(message: telebot.types.Message):
            if message.contact is not None:
                db.add_phone(message.from_user.id, message.contact.phone_number)


    def start_polling(self):
        self.__bot.polling(none_stop=True, interval=0)

    