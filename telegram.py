import re

import telebot

import db
import vk_helper
from config import conf

token = conf.read_config(["telegramtoken"])[0]
bot = telebot.TeleBot(token)


def platform_selector(platform):
    if platform == 0:
        return ""
    if platform == 1:
        return "Мобильная версия сайта"
    if platform == 2:
        return "Приложение для Iphone"
    if platform == 3:
        return "Приложение для iPad"
    if platform == 4:
        return "Приложение для Android"
    if platform == 5:
        return "Приложение для Windows Phone"
    if platform == 6:
        return "Приложение для Windows 10"
    if platform == 7:
        return "Полная версия сайта"


def send_online_message(first_name, last_name, telegram_id, platform):
    for chat_id in telegram_id:
        bot.send_message(chat_id, "[{0} {1}] В сети!\n{2}".format(first_name, last_name, platform_selector(platform)))


@bot.message_handler(commands=['start', 'help'])
def send_hello(message):
    bot.reply_to(message, "Приветствую друг!\nЯ помогу тебе отслеживать онлайн жертв\nВведите /spy что бы начать.")


def spy_next_step(msg):
    short_name = re.search("vk.com\/(.*)", msg.text)
    if short_name is None:
        return bot.reply_to(msg, "❌ Ой... Не верная ссылка")
    user_id = vk_helper.vk_session.get_id(short_name.group(1))
    vk = db.Vk.get_or_none(vk_id=user_id)
    if vk is None:
        vk = db.Vk.create(vk_id=user_id)
    tg = db.Telegram.get_or_none(telegram_id=msg.chat.id, vk=vk)
    if tg is None:
        db.Telegram.create(telegram_id=msg.chat.id, vk=vk)
    bot.reply_to(msg, "✅ ОК! Мы начали следить за жертвой.")


@bot.message_handler(commands=['spy'])
def spy(message):
    msg = bot.reply_to(message, "Что бы начать следить за жертвой, отправьте ссылку на пользователя\nНапример "
                                "https://vk.com/1")
    bot.register_next_step_handler(msg, spy_next_step)


def go_polling():
    bot.polling(none_stop=True)
