from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/filmstrip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    password = db.Column(db.BINARY(length=60))
    needsNewToken = db.Column(db.Boolean, default=False)
    registrationMethod = db.Column(db.String(255), default="username")

class Albums(db.Model):
    albumId = db.Column(db.Integer, primary_key=True)
    albumName = db.Column(db.String(255))
    userID = db.Column(db.Integer)
    albumDescription = db.Column(db.String(255))
    albumCamera = db.Column(db.String(255))
    albumFormat = db.Column(db.String(255), default="35mm")
    albumFilm = db.Column(db.String(255))

for item in Users.query.all():
    print(item.username)

print(Albums.query.filter_by(albumName='Better Name :)').first().albumName)