from flask import Flask
from testDB import db
from albumsTest import albumsBlueprintTest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/filmstrip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(albumsBlueprintTest)


testJson = {
    "username": "test",
    "firstName": "test",
    "lastName": "test",
    "email": "fake@gmail.com",
}

#testUser = Users(username="me3", email="rwarner322@gatech.edu", password=b'123')
#db.session.add(testUser)
#db.session.commit()

#for item in Users.query.all():
#    for album in item.albums:
#        print(album.albumDescription)

#print(Albums.query.filter_by(albumName='Better Name :)').first().albumName)