from datetime import datetime
from infrastructure import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    published_at = db.Column(db.DateTime(), default=datetime.utcnow())

    def save(self):
        db.session.add(self)
        db.session.commit()
