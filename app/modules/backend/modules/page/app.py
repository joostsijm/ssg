
"""
Backend
"""

from flask_login import login_required, current_user
from flask_menu import register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app import db
from app.models import Page


BLUEPRINT = Blueprint(
    'backend_page',
    __name__,
    template_folder='templates'
)


@BLUEPRINT.route('/create', methods=["GET", "POST"])
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


@BLUEPRINT.route('/edit/<int:page_id>', methods=["GET", "POST"])
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


@BLUEPRINT.route('/remove/<int:page_id>')
@login_required
def remove_page(page_id):
    """Page removing"""
    page = Page.query.get(page_id)

    db.session.delete(page)
    db.session.commit()

    flash('Page "%s" successfully remove' % page.title, 'success')
    return redirect(url_for('backend.index'))


@BLUEPRINT.route('/view/<int:page_id>')
@login_required
def view_page(page_id):
    """Display page"""
    page = Page.query.get(page_id)
    return render_template('page/view.j2', page=page)
