from flask import Flask, request

app = Flask(__name__)

@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    return {"token": "logging in"}

@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return {"string": "Logging out user."}

@app.route("/api/v1/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        return {
            "name": "Ryan Warner",
            "username": "ryan-warner",
            "email": "ryan.warner@gatech.edu"
        }
    else:
        return {"string": "Creating user."}

@app.route("/api/v1/user/photos", methods=["GET"])
def getPhotos():
    return {"string": "Getting photos."}