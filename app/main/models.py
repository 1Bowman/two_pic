from app import db


class Post(db.Model):
    __tablename__ = 'USER_POSTS'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    email = db.Column(db.String(64))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    description = db.Column(db.String(140), nullable=True)

    def __repr__(self):
        return '<Post {}>'.format(self.id)

