# -*- coding: utf-8 -*-

from flask import Flask
from flask_socketio import SocketIO

import threading
import time

# Блокировщик
threadLock = threading.Lock()
# Время ожидания (в секундах)
timeout = 1 * 60

app = Flask(__name__)
socket_ = SocketIO(app, async_mode='threading')

# Фоновый контроллер
def backgoundTask():

    time.sleep(timeout)


if __name__ == '__main__':

    bgTask = threading.Thread(target=backgoundTask)
    bgTask.daemon = True
    bgTask.start()

    socket_.run(app, host='localhost', debug=True, port=15000)