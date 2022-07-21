from flask import Flask
from flask_cors import CORS
from auth import authBlueprint
from user import userBlueprint
from albums import albumsBlueprint
# export FLASK_DEBUG=1
# flask run -h localhost -p 4000

app = Flask(__name__)
CORS(app)

app.register_blueprint(authBlueprint)
app.register_blueprint(userBlueprint)
app.register_blueprint(albumsBlueprint)


@app.route("/api/v1/user/photos", methods=["GET"])
def getPhotos():
    return {"string": "Getting photos."}