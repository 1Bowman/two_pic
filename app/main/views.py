import os
from flask import render_template, session, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
from . import main
from .forms import UploadForm
from .. import db
# from ..models import User

basedir = os.path.abspath(os.path.dirname(__file__))

@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # return 'hello'
    return render_template('index.html')


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        print('==== {}'.format(image.filename.split('.')[1]))
        if image and image.filename.split('.')[1] in ['jpg', 'jpeg', 'png', 'bmp']:
            print('=== shit')
            filename = secure_filename(image.filename)
            image.save(os.path.join(basedir, 'user_content', filename))
            return redirect(url_for('main.uploaded_file', filename=filename))
    else:
        form = UploadForm()
        return render_template('upload.html', form=form)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(os.path.join(basedir, 'user_content'), filename)


@main.route('/<name>')
def name_yeah(name):
    return '<h1>{} is a bitch.<h1>'.format(name)
