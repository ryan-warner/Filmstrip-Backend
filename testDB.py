from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Users(db.Model):
    __tablename__ = 'users'
    userID: int
    username: str
    email: str
    firstName: str
    lastName: str
    needsNewToken: bool
    registrationMethod: str
    albums: list

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    password = db.Column(db.BINARY(length=60), nullable=False)
    needsNewToken = db.Column(db.Boolean, default=False)
    registrationMethod = db.Column(db.String(255), default="username")
    albums = db.relationship("Albums", backref="user")

@dataclass
class Albums(db.Model):
    __tablename__ = 'albums'
    albumID: int
    albumName: str
    userID: int
    albumDescription: str
    albumCamera: str
    albumFormat: str
    albumFilm: str
    
    albumID = db.Column(db.Integer, primary_key=True)
    albumName = db.Column(db.String(255))
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    albumDescription = db.Column(db.String(255))
    albumCamera = db.Column(db.String(255))
    albumFormat = db.Column(db.String(255), default="35mm")
    albumFilm = db.Column(db.String(255))