from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db

class Song(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True)
    artists = db.Column(db.String(128), index=True)
    uri = db.Column(db.String(128), index=True)

    def __repr__(self):
        return '<Song \'%s\'>' % self.name

class UserChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    rank = db.Column(db.Integer)

    def __repr__(self):
        return '<Song \'%s\'>' % self.name