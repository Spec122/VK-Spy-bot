import threading

from telegram import go_polling
from vk_helper import vk_session


def main():
    online = threading.Thread(target=vk_session.check_online, args=())
    polling = threading.Thread(target=go_polling, args=())
    polling.start()
    online.start()


main()
