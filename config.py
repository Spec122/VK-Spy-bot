import configparser
import os

config_path = "config.ini"
tg_token = "TELEGRAMTOKEN"
access_token = "ACCESSTOKEN"
vk_login = "VKLOGIN"
vk_password = "VKPASSWORD"
appid = "APPID"


class Config:
    def __init__(self):
        if not os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.add_section(config_path)
            config.set(config_path, access_token, "")
            config.set(config_path, vk_login, "")
            config.set(config_path, vk_password, "")
            config.set(config_path, appid, "2685278")
            config.set(config_path, tg_token, "")

            with open(config_path, "w") as config_file:
                config.write(config_file)

    def read_config(self, params):
        config = configparser.ConfigParser()
        config.read(config_path)
        keys = []
        for i in range(len(params)):
            keys.append(config.get(config_path, params[i]))
        return keys

    def set_config(self, tag, key):
        config = configparser.ConfigParser()
        config.set(config_path, tag, key)

        with open(config_path, "w") as config_file:
            config.write(config_file)


conf = Config()
