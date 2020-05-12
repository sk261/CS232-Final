from flask import Flask
app = Flask(__name__)
from app import routes

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def _random_key():
    key = ''
    return key