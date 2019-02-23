
"""
Simple flask thing
"""

from flask_login import login_required, login_user, logout_user
from flask_menu import register_menu
from flask import render_template, request, redirect, url_for, flash
from app import app, login_manager, db
from app.models import User
from app.modules.static import Static
from app.modules.backend import Backend
from app.modules.auth import Auth

app.register_blueprint(Auth)
app.register_blueprint(Static)
app.register_blueprint(Backend, url_prefix='/backend')
