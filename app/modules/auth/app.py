
"""
Authentication module
"""

import os

from flask_login import login_required, login_user, logout_user, current_user
from flask_menu import Menu, register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort, jsonify
from jinja2 import TemplateNotFound
from app import app, login_manager, db
from app.models import User, Page


BLUEPRINT = Blueprint(
    'auth',
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
        if user:
            if not user.approved:
                flash('Account not approved yet.', 'warning')
            if user.check_password(password):
                login_user(user, remember=True)
                flash('Successfully loggend in.', 'success')
                if request.args.get("next"):
                    return redirect(request.args.get('next'))
                return redirect(url_for('backend.index'))
            flash('Password Incorrect.', 'warning')
            return render_template('login.j2', login_email=email)
        flash('Email not found.', 'warning')
    return render_template('login.j2')


@BLUEPRINT.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    name = request.form['name'] if 'name' in request.form else None
    email = request.form['email'] if 'email' in request.form else None
    password = request.form['password'] if 'email' in request.form else None

    if name is None:
        flash('Fill in the name.', 'warning')
        return render_template('login.j2')

    if email is None:
        flash('Fill in the email.', 'warning')
        return render_template(
            'login.j2',
            name=name
        )

    if password is None:
        flash('Fill in the password.', 'warning')
        return render_template(
            'login.j2',
            name=name,
            email=email
        )

    user = User.query.filter(User.email == email).first()
    if user is not None:
        flash('Email already taken.', 'warning')
        return render_template(
            'login.j2',
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
    return redirect(url_for('static.index'))


@BLUEPRINT.route("/logout")
@login_required
def logout():
    """Logout function for users"""
    logout_user()
    return redirect(url_for('static.show'))
