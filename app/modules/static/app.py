
"""
Serve static content
"""

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
    try:
        if current_user.is_authenticated:
            return render_template("private/%s.html" % page)
        return render_template("public/%s.html" % page)
    except TemplateNotFound:
        abort(404)
