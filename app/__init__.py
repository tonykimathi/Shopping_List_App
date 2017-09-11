from flask import Flask
from flask_bootstrap import Bootstrap
from app.models import Data


app = Flask(__name__)
Bootstrap(app)

from app import views

app.config.from_object('config')