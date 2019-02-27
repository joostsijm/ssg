
"""
Backend
"""

import os

from flask_login import login_required
from flask_menu import register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.models import Page, File


BLUEPRINT = Blueprint(
    'backend',
    __name__,
    template_folder='templates'
)


@BLUEPRINT.route('/')
@register_menu(BLUEPRINT, 'index', 'Home')
@login_required
def index():
    """Show homepage"""
    pages = Page.query.all()
    files = File.query.all()
    return render_template(
        'site/index.j2',
        pages=pages,
        files=files
    )


@BLUEPRINT.route('/render')
@register_menu(BLUEPRINT, 'render', 'Render')
@login_required
def render():
    """Render pages to file"""
    pages = Page.query.filter(Page.parent_id == None).all()
    menu = []
    for page in pages:
        menu.append(generate_menu(page))

    path_base = 'app/modules/static/pages/'
    for page in pages:
        render_page(path_base, page, menu)

    flash('Successfully rendered pages.', 'success')
    return redirect(request.referrer, code=302)


def generate_menu(page):
    """Generate menu based on pages"""
    menu_item = {}
    menu_item['title'] = page.title
    menu_item['url'] = page.path()
    if page.children.count():
        menu_item['children'] = []
        for child_page in page.children:
            menu_item['children'].append(generate_menu(child_page))
    return menu_item


def render_page(path, page, menu):
    """Function for page generation, recursive"""
    if not page.private and not page.parent_id:
        path += 'public/' + page.url()
    else:
        path += page.url()
    if page.children.count():
        parent_path = path + '/'
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        for child_page in page.children:
            render_page(parent_path, child_page, menu)

    with open('%s.html' % path, 'w') as file:
        rendered_page = render_template(
            'public/site.j2',
            page=page,
            menu=menu
        )
        file.write(rendered_page)
