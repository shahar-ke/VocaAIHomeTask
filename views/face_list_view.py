import os

from flask import Blueprint, request, flash, render_template, url_for
from flask_api import status
from werkzeug.utils import redirect, secure_filename

from app import app

face_list_view = Blueprint('face_list_view', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@face_list_view.route('/face_list/upload', methods=['POST'])
def upload_images():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(url_for('index_view.index')), status.HTTP_400_BAD_REQUEST
    files = request.files.getlist('files[]')
    file_names = []
    files = [file for file in files if file is not None]
    for file in files:
        if not allowed_file(file.filename):
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(url_for('index_view.index')), status.HTTP_400_BAD_REQUEST
    for file in files:
        try:
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            return render_template('error.html', error_msg=f'could not save {file}, {str(e)}'), \
                   status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    return render_template('upload.html', filenames=file_names, action='uploaded')


@face_list_view.route('/face_list/delete', methods=['POST'])
def delete_images():
    upload_folder = app.config['UPLOAD_FOLDER']
    deleted_files = list()
    for filename in os.listdir(upload_folder):
        try:
            if not allowed_file(filename):
                continue
            file_path = os.path.join(upload_folder, filename)
            os.remove(file_path)
            deleted_files.append(filename)
        except Exception as e:
            return render_template('error.html', error_msg=f'could not delete {filename}, {str(e)}'), \
                   status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    return render_template('upload.html', filenames=deleted_files, action='deleted')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
