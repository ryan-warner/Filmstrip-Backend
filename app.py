from flask import Flask
from database import db
from albums import albumsBlueprint
from user import userBlueprint
from auth import authBlueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/filmstrip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(albumsBlueprint)
app.register_blueprint(userBlueprint)
app.register_blueprint(authBlueprint)