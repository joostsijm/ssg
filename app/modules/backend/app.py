
"""
Backend
"""

import os
import shutil

from flask_login import login_required
from flask_menu import register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.models import Page, File, User


BLUEPRINT = Blueprint(
    'backend',
    __name__,
    template_folder='templates'
)

BASE_PATH = 'app/modules/static/pages/'

@BLUEPRINT.route('/')
@register_menu(BLUEPRINT, 'index', 'Home')
@login_required
def index():
    """Show homepage"""
    pages = Page.query.filter(Page.parent_id == None).all()
    files = File.query.all()
    users = User.query.all()
    return render_template(
        'site/index.j2',
        pages=pages,
        files=files,
        users=users
    )


@BLUEPRINT.route('/render')
@register_menu(BLUEPRINT, 'render', 'Render')
@login_required
def render():
    """Render pages to file"""
    pages = Page.query.filter(Page.parent_id == None).all()
    menu = []
    for page in pages:
        if page.title != 'index':
            menu.append(generate_menu(page))

    path_base = 'app/modules/static/pages/'
    path_public = path_base + "public"
    path_private = path_base + "private"
    if os.path.exists(path_public):
        shutil.rmtree(path_public)
    os.makedirs(path_public)
    if os.path.exists(path_private):
        shutil.rmtree(path_private)
    os.makedirs(path_private)

    for page in pages:
        generate_directory('', page)

    for page in pages:
        render_page('', page, menu)

    flash('Successfully rendered pages.', 'success')
    return redirect(request.referrer, code=302)


def generate_menu(page):
    """Generate menu based on pages"""
    menu_item = {}
    menu_item['title'] = page.title
    menu_item['url'] = page.path()
    menu_item['private'] = page.private
    if page.children.count():
        menu_item['children'] = []
        for child_page in page.children:
            menu_item['children'].append(generate_menu(child_page))
    return menu_item


def generate_directory(path, page):
    """Generate directories for pages"""
    if page.children.count():
        parent_path = path + page.url() + '/'
        public_path = BASE_PATH + 'public/' + path + page.url()
        private_path = BASE_PATH + 'private/' + path + page.url()
        if not os.path.exists(public_path):
            os.makedirs(public_path)
        if not os.path.exists(private_path):
            os.makedirs(private_path)
        for child_page in page.children:
            generate_directory(parent_path, child_page)


def render_page(path, page, menu):
    """Function for page generation, recursive"""
    if page.children.count():
        path += page.url() + '/'
        for child_page in page.children:
            render_page(path, child_page, menu)

    path += page.url()

    # private
    private_path = '%s%s/%s.html' % (BASE_PATH, 'private', path)
    with open(private_path, 'w') as file:
        rendered_page = render_template(
            'public/private.j2',
            page=page,
            menu=menu
        )
        file.write(rendered_page)

    public_path = '%s%s/%s.html' % (BASE_PATH, 'public', path)
    with open(public_path, 'w') as file:
        rendered_page = render_template(
            'public/public.j2',
            page=page,
            menu=menu
        )
        file.write(rendered_page)
