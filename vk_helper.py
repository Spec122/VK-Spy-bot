import vk_api
import json
import exceptions
from config import conf
from db import Vk, Telegram
from telegram import send_online_message
import time


class VkHelper:
    def __init__(self, login="", password="", token="", appid=""):
        vk_session = None
        if login and password:
            vk_session = vk_api.VkApi(login, password, app_id=appid)
            vk_session.auth()
        elif token:
            vk_session = vk_api.VkApi(token=token, app_id=appid)
        else:
            raise exceptions.NoCredentials
        self.vk_session = vk_session.get_api()
        print("Successful auth")

    def get_id(self, shortname):
        user = self.vk_session.users.get(ids=shortname)
        return user[0]["id"]

    def get_user_info(self, users_ids):
        return self.vk_session.users.get(user_ids=users_ids, fields="online, last_seen")

    def check_online(self):
        while True:
            vk_ids = []
            for vk in Vk.select():
                vk_ids.append(vk.vk_id)
            user_info = self.get_user_info(vk_ids)
            for user in user_info:
                if user["online"]:
                    vk = Vk.get(vk_id=user["id"])
                    telegram_ids = []
                    for tg in Telegram.select().where(Telegram.vk == vk):
                        telegram_ids.append(tg.telegram_id)
                    if user["last_seen"]["time"] == vk.last_seen:
                        continue
                    if user["last_seen"]["time"] - int(vk.last_seen) < 300:
                        continue
                    last_seen, platform = user["last_seen"]["time"], user["last_seen"]["platform"]
                    first_name, last_name = user["first_name"], user["last_name"]
                    vk.last_seen = last_seen
                    vk.save()
                    send_online_message(first_name, last_name, telegram_ids, platform)
                    time.sleep(60)


login, password, token, appid = \
    conf.read_config(["VKLOGIN", "VKPASSWORD", "ACCESSTOKEN", "APPID"])
vk_session = VkHelper(login, password, token, appid)