
"""
Initialize the modules needed for the website
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_compress import Compress
from flask_argon2 import Argon2
from flask_menu import Menu
from dotenv import load_dotenv


load_dotenv()

class Config(object):
    """Flask configuration"""
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 1296000


app = Flask(__name__)
app.config.from_object(Config())
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

# Compress settings
COMPRESS_MIMETYPES = [
    'text/html',
    'text/css',
    'text/xml',
    'application/json',
    'application/javascript'
]
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)
Menu(app=app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
argon2 = Argon2(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
