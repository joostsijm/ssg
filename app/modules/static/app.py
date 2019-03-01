
"""
Serve static content
"""

import os
from flask import render_template, Blueprint, abort
from jinja2 import TemplateNotFound
from flask_login import current_user


BLUEPRINT = Blueprint(
    "static",
    __name__,
    template_folder='pages'
)

@BLUEPRINT.route("/", defaults={"page": "index"})
@BLUEPRINT.route("/<path:page>")
def show(page):
    """Display static page"""
    if current_user.is_authenticated:
        try:
            return render_template("private/%s.html" % page)
        except TemplateNotFound:
            abort(404)
    try:
        return render_template("public/%s.html" % page)
    except TemplateNotFound:
        if os.path.exists("app/modules/static/pages/private/%s.html" % page):
            abort(401)
        abort(404)
