from flask import Flask
from os import getenv


app = Flask(__name__)
# app.secret_key = getenv("SECRET_KEY")
app.secret_key = "test"

import routes
