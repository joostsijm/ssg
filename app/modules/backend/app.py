
"""
Backend
"""

import os

from flask_login import login_required, login_user, logout_user, current_user
from flask_menu import Menu, register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort, jsonify
from jinja2 import TemplateNotFound
from app import app, login_manager, db
from app.models import User, Page


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
    pages = Page.query.filter(Page.parent_id == None).all()
    return render_template('site/index.j2', pages=pages)


@BLUEPRINT.route('/page/create', methods=["GET", "POST"])
@register_menu(BLUEPRINT, 'page_create', 'Create page')
@login_required
def create_page():
    """Page creating"""
    pages = Page.query.all()
    if request.method == 'POST':
        page = Page()
        page.title = request.form['title']
        page.source = request.form['source']
        page.user_id = current_user.id
        page.parent_id = request.form['parent_id'] if request.form['parent_id'] else None

        db.session.add(page)
        db.session.commit()

        flash('Page "%s" successfully created' % page.title, 'success')

    return render_template('page/create.j2', pages=pages)


@BLUEPRINT.route('/page/edit/<int:page_id>', methods=["GET", "POST"])
@login_required
def edit_page(page_id):
    """Page editing"""
    page = Page.query.get(page_id)
    pages = Page.query.filter(Page.id != page.id).all()

    if request.method == 'POST':
        page.title = request.form['title']
        page.source = request.form['source']
        page.parent_id = request.form['parent_id'] if request.form['parent_id'] else None
        page.user_id = current_user.id

        db.session.add(page)
        db.session.commit()

        flash('Page "%s" successfully edit' % page.title, 'success')

    return render_template(
        'page/edit.j2',
        page=page,
        pages=pages
    )


@BLUEPRINT.route('/page/remove/<int:page_id>')
@login_required
def remove_page(page_id):
    """Page removing"""
    page = Page.query.get(page_id)

    db.session.delete(page)
    db.session.commit()

    flash('Page "%s" successfully remove' % page.title, 'success')
    return redirect(url_for('backend.index'))


@BLUEPRINT.route('/page/view/<int:page_id>')
@login_required
def view_page(page_id):
    """Display page"""
    page = Page.query.get(page_id)
    return render_template('page/view.j2', page=page)


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
    return redirect(url_for('backend.index'))


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
    path = path + page.url()
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
