
"""
Backend
"""

import os
from flask_login import login_required, current_user
from flask_menu import register_menu
from flask import render_template, request, redirect, url_for, flash, Blueprint
from werkzeug.utils import secure_filename
from app import app, db
from app.models import File



BLUEPRINT = Blueprint(
    'backend_file',
    __name__,
    template_folder='templates'
)

def allowed_file(filename):
    allowed_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@BLUEPRINT.route('/create', methods=["GET", "POST"])
@register_menu(BLUEPRINT, 'create_file', 'Create file')
@login_required
def create():
    """File creating"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            db_file = File()
            if request.form['title']:
                title = request.form['title'] 
            else:
                title = file.filename
            db_file.title = title 
            db_file.user_id = current_user.id
            db_file.path = file.filename

            db.session.add(db_file)
            db.session.commit()

            flash('File "%s" successfully uploaded' % db_file.title, 'success')
            return redirect(url_for('backend_file.view', file_id=db_file.id))

    return render_template('file/create.j2')


@BLUEPRINT.route('/edit/<int:file_id>', methods=["GET", "POST"])
@login_required
def edit(file_id):
    """File editing"""
    db_file = File.query.get(file_id)

    if request.method == 'POST':
        file = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'warning')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        if file is not None:
            db_file.path = file.filename
        if request.form['title']:
            db_file.title = request.form['title']
        else:
            db_file.title = db_file.path

        db_file.user_id = current_user.id

        db.session.add(db_file)
        db.session.commit()

        flash('File "%s" successfully edit' % db_file.title, 'success')

    return render_template(
        'file/edit.j2',
        file=db_file,
    )


@BLUEPRINT.route('/remove/<int:file_id>')
@login_required
def remove(file_id):
    """File removing"""
    file = File.query.get(file_id)

    db.session.delete(file)
    db.session.commit()

    flash('File "%s" successfully remove' % file.title, 'success')
    return redirect(url_for('backend.index'))


@BLUEPRINT.route('/view/<int:file_id>')
@login_required
def view(file_id):
    """Display file"""
    file = File.query.get(file_id)
    return render_template('file/view.j2', file=file)
