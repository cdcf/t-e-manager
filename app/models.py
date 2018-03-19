__author__ = 'Cedric Da Costa Faro'

from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class Permission:
    FOLLOW = 0x01
    WRITE = 0x04
    MODERATE = 0x08
    ADMIN = 0x80


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.WRITE, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.WRITE |
                          Permission.MODERATE, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='user_task', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    clients = db.relationship('Client', backref='user_client', lazy='dynamic')
    projects = db.relationship('Project', backref='user_project', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['TIME_TRACKER_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_tasks(self):
        followed = Task.query.join(
            followers, (followers.c.followed_id == Task.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Task.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Task.date.desc())

    def my_tasks(self):
        own = Task.query.filter_by(user_id=self.id)
        return own.order_by(Task.date.desc(), Task.client_id.asc(), Task.jira.asc())

    def get_reset_password_token(self, expires_in=60):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_administrator(self):
        return False

login.anonymous_user = AnonymousUser

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jira = db.Column(db.String(16))
    duration = db.Column(db.Numeric(4,2))
    date = db.Column(db.Date, index=True)
    comment = db.Column(db.String(240))
    rate = db.Column(db.Numeric(6,2))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Task {}>'.format(self.name)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='project_task', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        return '<Project>'.format(self.name)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='client_task', lazy='dynamic')
    projects = db.relationship('Project', backref='client_project', lazy='dynamic')

    def __repr__(self):
        return '<Client>'.format(self.name)