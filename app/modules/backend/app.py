
"""
Backend
"""

import os

from flask_login import login_required, login_user, logout_user, current_user
from flask_menu import Menu, register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from jinja2 import TemplateNotFound
from app import app, login_manager, db
from app.models import User, Page


BLUEPRINT = Blueprint(
    'backend',
    __name__,
    template_folder='templates'
)

@BLUEPRINT.route("/login", methods=["GET", "POST"])
def login():
    """Handle login page and data"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter(User.email == email).first()
        if user is not None:
            if user.check_password(password):
                login_user(user, remember=True)
                flash('You were successfully logged in.', 'success')
                if request.args.get("next") is not None:
                    return redirect(request.args.get("next"))
                return redirect(url_for('backend.index'))
            flash('Incorrect password.', 'danger')
        else:
            flash('User not found.', 'danger')
        return redirect(url_for('backend.login'))
    return render_template('user/login.j2')


@BLUEPRINT.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    name = request.form['name'] if 'name' in request.form else None
    email = request.form['email'] if 'email' in request.form else None
    password = request.form['password'] if 'email' in request.form else None

    if name is None:
        flash('Fill in the name.', 'warning')
        return render_template('user/login.j2')

    if email is None:
        flash('Fill in the email.', 'warning')
        return render_template(
            'user/login.j2',
            name=name
        )

    if password is None:
        flash('Fill in the password.', 'warning')
        return render_template(
            'user/login.j2',
            name=name,
            email=email
        )

    user = User.query.filter(User.email == email).first()
    if user is not None:
        flash('Email already taken.', 'warning')
        return render_template(
            'user/login.j2',
            name=name,
        )

    user = User()
    user.name = name
    user.email = email
    user.password = password

    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    flash('Successfully registered account "%s".' % (user.name), 'success')

    if request.args.get("next") is not None:
        return redirect(request.args.get("next"))
    return redirect(url_for('backend.index'))


@BLUEPRINT.route("/logout")
@login_required
def logout():
    """Logout function for users"""
    logout_user()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('backend.login'))


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
    path_base = 'app/modules/static/pages/'
    for page in pages:
        render_page(path_base, page)

    flash('Successfully rendered pages.', 'success')
    return redirect(url_for('backend.index'))

def render_page(path, page):
    """Function for page generation, recursive"""
    path = path + page.url()
    if page.children.count():
        parent_path = path + '/'
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        for child_page in page.children:
            render_page(parent_path, child_page)

    with open('%s.html' % path, 'w') as file:
        rendered_page = render_template(
            'public/site.j2',
            page=page,
        )
        file.write(rendered_page)
