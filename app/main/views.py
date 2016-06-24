import os
from flask import render_template, session, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from . import main
from .forms import UploadForm
from app import db
from app.main.models import Post

basedir = os.path.abspath(os.path.dirname(__file__))

@main.route('/', methods=['GET', 'POST'])
def index():
    picture1 = Post.query.get(1)
    picture2 = Post.query.get(2)

    picture1 = url_for('static', filename=picture1.filename)
    picture2 = url_for('static', filename=picture2.filename)

    return render_template('index.html', pic1=picture1, pic2=picture2)


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)

        # Check that an image was attached
        image = request.files['image']

        if image.filename == '':
            return redirect(request.url)

        if image and image.filename.split('.')[1] in ['jpg', 'jpeg', 'png', 'bmp']:
            # name and save the file
            filename = secure_filename(image.filename)
            image.save(os.path.join(basedir, 'static', filename))

            # add our new post to the database
            post = Post(datetime=datetime.utcnow(), email=form.email.data,
                        first_name=form.first_name.data, last_name=form.last_name.data,
                        description=form.description.data, filename=filename)

            db.session.add(post)

            return redirect(url_for('main.uploaded_file', filename=filename))
    else:
        return render_template('upload.html', form=form)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(os.path.join(basedir, 'user_content'), filename)


@main.route('/<name>')
def name_yeah(name):
    return '<h1>{} is a bitch.<h1>'.format(name)
