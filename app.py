from flask import Flask
from auth import authBlueprint
from user import userBlueprint
# export FLASK_DEBUG=1

app = Flask(__name__)

app.register_blueprint(authBlueprint)
app.register_blueprint(userBlueprint)

@app.route("/api/v1/user/photos", methods=["GET"])
def getPhotos():
    return {"string": "Getting photos."}
