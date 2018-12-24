
"""
Simple flask thing
"""

from flask_login import login_required, login_user, logout_user
from flask_menu import Menu, register_menu
from flask import render_template, request, redirect, url_for, flash
from app import app, login_manager, db
from app.models import User

Menu(app=app)


@login_manager.user_loader
def load_user(user_id):
    """Return user"""
    return User.query.get(user_id)


@app.route("/login", methods=["GET", "POST"])
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
            else:
                flash('Incorrect password.', 'danger')
        else:
            flash('User not found.', 'danger')

        return redirect(url_for('login'))
    else:
        return render_template('user/login.html')


@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    if request.method != "POST":
        return redirect(url_for('login'))

    if "name" not in request.form or not request.form['name']:
        flash('Fill in the name.', 'warning')
        return render_template('user/login.html')

    if "email" not in request.form or not request.form['email']:
        flash('Fill in the email.', 'warning')
        return render_template('user/login.html', name=request.form['name'])

    if "password" not in request.form or not request.form['password']:
        flash('Fill in the password.', 'warning')
        return render_template(
            'user/login.html',
            name=request.form['name'],
            email=request.form['email']
        )

    user = User.query.filter(User.name == request.form['name']).first()
    if user is None:
        flash('Name not found.', 'warning')
        return render_template(
            'user/login.html',
            name=request.form['name'],
            email=request.form['email']
        )

    if user.email is not None:
        flash('User already taken.', 'warning')
        return render_template(
            'user/login.html',
            name=request.form['name'],
            email=request.form['email']
        )

    user.email = request.form['email']
    user.password = request.form['password']

    db.session.commit()
    login_user(user, remember=True)
    flash('Succesfully registered account "%s".' % (user.name), 'success')

    if request.args.get("next") is not None:
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    """Logout function for users"""
    logout_user()
    flash('succesfully logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/')
@register_menu(app, '.', 'Home')
def index():
    """Show homepage"""

    return render_template('site/index.html')
