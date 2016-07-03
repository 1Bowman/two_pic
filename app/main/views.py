import os
from flask import render_template, session, redirect, url_for, request, send_from_directory, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from . import main
from .forms import UploadForm
from app import db
from app.main.models import Post
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
from config import basedir
from random import randint


@main.route('/', methods=['GET', 'POST'])
def index():

    # Grab the choice variable passed from POST
    # for x in request.args['choice']:
    #   print('in args: {}'.format(x))

    # hook up database functions
    Session = sessionmaker()

    # locate the db location; currently hardcoded to development database
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))
    Session.configure(bind=engine)
    session = Session()

    post_count = session.query(func.count(Post.id)).scalar()  # count number of unique posts in the table
    pic1 = Post.query.get(randint(1, post_count))  # fails if there is 1 or less entries in the database
    pic2 = None
    while pic2 == pic1 or pic2 is None:  # Don't pick the same file
        pic2 = Post.query.get(randint(1, post_count))

    pic1_filename = url_for('static', filename=pic1.filename)
    pic2_filename = url_for('static', filename=pic2.filename)

    return render_template('index.html', pic1=pic1, pic2=pic2, pic1_filename=pic1_filename, pic2_filename=pic2_filename)


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

        # Check that our filename is in the 'approved' array
        if image and image.filename.split('.')[1] in ['jpg', 'jpeg', 'png', 'bmp']:
            # name and save the file
            filename = secure_filename(image.filename)
            image.save(os.path.join(basedir, 'app', 'static', filename))

            # add our new post to the database
            post = Post(datetime=datetime.utcnow(), email=form.email.data,
                        first_name=form.first_name.data, last_name=form.last_name.data,
                        description=form.description.data, filename=filename)

            db.session.add(post)
            flash(form.description.data)
            return redirect(url_for('main.index'))
    else:
        return render_template('upload.html', form=form)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(basedir, 'app', 'static'), filename)


@main.route('/choice/<winner>-<loser>')
def update_count(winner, loser):
    Session = sessionmaker()
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))
    Session.configure(bind=engine)
    session = Session()

    curr_usr = session.query(Post).get(winner)
    loser_guy = session.query(Post).get(loser)
    session.query(Post).filter_by(id=winner).update({'total_votes': curr_usr.total_votes+1})
    session.commit()
    flash("{} has {} votes and {} has {} votes".format(curr_usr.description, curr_usr.total_votes, loser_guy.description, loser_guy.total_votes))
    return redirect(url_for('main.index'))


@main.route('/<name>')
def name_yeah(name):
    return '<h1>{} is a bitch.<h1>'.format(name)
