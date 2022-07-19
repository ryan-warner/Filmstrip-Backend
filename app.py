from flask import Flask

app = Flask(__name__)

@app.route("/api/v1/getProfile")
def getProfile():
    return {"string": "Hello world!"}

@app.route("/api/v1/getProfile")
def getProfile():
    return {"string": "Hello world!"}