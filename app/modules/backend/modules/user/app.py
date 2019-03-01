
"""
Backend
"""

from flask_login import login_required, current_user
from flask_menu import register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app import db
from app.models import User


BLUEPRINT = Blueprint(
    'backend_user',
    __name__,
    template_folder='templates'
)


@BLUEPRINT.route('/edit/<int:user_id>', methods=["GET", "POST"])
@login_required
def edit(user_id):
    """User editing"""
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.name = request.form['name']

        db.session.add(user)
        db.session.commit()

        flash('User "%s" successfully edit' % user.name, 'success')

    return render_template(
        'user/edit.j2',
        user=user,
    )


@BLUEPRINT.route('/approve/<int:user_id>')
@login_required
def approve(user_id):
    """User removing"""
    user = User.query.get(user_id)
    user.approved = True

    db.session.add(user)
    db.session.commit()

    flash('User "%s" successfully approved.' % user.name, 'success')
    return redirect(url_for('backend.index'))


@BLUEPRINT.route('/remove/<int:user_id>')
@login_required
def remove(user_id):
    """User removing"""
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    flash('User "%s" successfully remove' % user.name, 'success')
    return redirect(url_for('backend.index'))


@BLUEPRINT.route('/view/<int:user_id>')
@login_required
def view(user_id):
    """Display user"""
    user = User.query.get(user_id)
    return render_template('user/view.j2', user=user)
