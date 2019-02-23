
"""
Serve static content
"""

from flask import render_template, Blueprint, abort
from jinja2 import TemplateNotFound


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
        return render_template("%s.html" % page)
    except TemplateNotFound:
        abort(404)
