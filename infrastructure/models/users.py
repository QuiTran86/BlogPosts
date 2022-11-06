import hashlib
from datetime import datetime

from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as JWS_Serializer
from itsdangerous.exc import SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager
from domain.permission import Permission
from infrastructure.models.posts import Post
from infrastructure.models.relationship import Follow
from infrastructure.models.roles import Role
from .. import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}
    CONFIRMED_TOKEN_EXPIRY = 300
    GRAVATAR_SERVICE_URI = 'https://secure.gravatar.com/avatar'

    id = db.Column(db.Integer, primary_key=True)
    avatar_file = db.Column(db.String(100))
    name = db.Column(db.String(64))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'), lazy='dynamic',
                                cascade='all, delete-orphan')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'), lazy='dynamic',
                               cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return f'{self.__class__.__name__}(username={self.username})'

    def avatar(self, size=100, default='identicon'):
        code = hashlib.md5(self.email.encode('utf8')).hexdigest()
        return f'{self.GRAVATAR_SERVICE_URI}/{code}?s={size}&d={default}'

    def can_do(self, permission):
        return self.role is not None and self.role.has_permission(permission)

    def confirm(self, token):
        serializer = JWS_Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token.encode('utf-8'))
        except SignatureExpired:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()
        return True

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            db.session.commit()

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(
            Follow.follower_id == self.id)

    def mark_as_forgot_password(self):
        self.confirmed = False
        self.save()

    def is_administrator(self):
        return self.role.name == Permission.ADMIN

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(follower_id=user.id).first() is None

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_valid_media_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSION

    def generate_confirmed_token(self):
        serializer = JWS_Serializer(secret_key=current_app.config['SECRET_KEY'],
                                    expires_in=self.CONFIRMED_TOKEN_EXPIRY)
        return serializer.dumps({'confirm': self.id}).decode('utf8')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('Attribute password can not be accessed!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


class AnonymousUser(AnonymousUserMixin):

    def can_do(self, permission):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
