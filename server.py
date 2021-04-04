# -*- coding: utf-8 -*-
"""
    Точка входа в приложение.

    author: Шамхалов Р.М.
"""
from flask import Flask, request, json
import hh
import base
from urllib.parse import urlparse
app = Flask(__name__)


@app.route('/check', methods=['GET'])
def check():
    return 200


if __name__ == '__main__':
    for cls in base.WorkPool.__subclasses__():
        cls.start_pool()
    app.run(debug=True, port=2001)
