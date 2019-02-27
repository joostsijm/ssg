
"""
Serve static content
"""

from flask import render_template, Blueprint, abort
from jinja2 import TemplateNotFound
from flask_login import login_required


BLUEPRINT = Blueprint(
    "static",
    __name__,
    template_folder='pages'
)

@BLUEPRINT.route("/private", defaults={"page": "index"})
@BLUEPRINT.route("/private/<path:page>")
@login_required
def private_show(page):
    """Display static page"""
    try:
        return render_template("private/%s.html" % page)
    except TemplateNotFound:
        abort(404)


@BLUEPRINT.route("/", defaults={"page": "index"})
@BLUEPRINT.route("/<path:page>")
def show(page):
    """Display static page"""
    try:
        return render_template("public/%s.html" % page)
    except TemplateNotFound:
        abort(404)
