from config import Config
import time
import threading
from vk_helper import vk_session
import db
from config import conf
from telegram import go_polling


def main():
    online = threading.Thread(target=vk_session.check_online, args=())
    polling = threading.Thread(target=go_polling, args=())
    polling.start()
    online.start()


main()


