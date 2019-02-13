
"""
Backend
"""

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
                return redirect(url_for('index'))
            flash('Incorrect password.', 'danger')
        else:
            flash('User not found.', 'danger')
        return redirect(url_for('login'))
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
    return redirect(url_for('login'))


@BLUEPRINT.route('/')
@register_menu(BLUEPRINT, 'index', 'Home')
@login_required
def index():
    """Show homepage"""
    pages = Page.query.all()
    return render_template('site/index.j2', pages=pages)


@BLUEPRINT.route('/page/create', methods=["GET", "POST"])
@register_menu(BLUEPRINT, 'page_create', 'Create page')
@login_required
def create_page():
    """Show creating page"""
    if request.method == 'POST':
        page = Page()
        page.title = request.form['title']
        page.source = request.form['source']
        page.user_id = current_user.id

        db.session.add(page)
        db.session.commit()

        flash('Page "%s" successfully created' % page.title, 'success')

    return render_template('page/create.j2')


@BLUEPRINT.route('/page/<int:page_id>')
def view_page(page_id):
    """Display page"""
    page = Page.query.get(page_id)
    return render_template('page/view.j2', page=page)
