from app import db


class Post(db.Model):
    __tablename__ = 'USER_POSTS'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    email = db.Column(db.String(64))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    description = db.Column(db.String(140), nullable=True)
    filename = db.Column(db.String(256))
    total_votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post {}>'.format(self.id)


# class Count(db.Model):
#     __tablename__  = 'COUNT_TBL'
#     count = db.Column(db.Integer)
