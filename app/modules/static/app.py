
"""
Serve static content
"""

from flask_login import login_required, login_user, logout_user
from flask_menu import Menu, register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from jinja2 import TemplateNotFound
from app import app, login_manager, db
from app.models import User


BLUEPRINT = Blueprint(
    "static",
    __name__,
)

@BLUEPRINT.route("/", defaults={"page": "index"})
@BLUEPRINT.route("/<path:page>")
def show(page):
    """Display static page"""
    try:
        return render_template("%s.html" % page)
    except TemplateNotFound:
        abort(404)
