from flask import request, Blueprint
from db import cursor
import bcrypt


authBlueprint = Blueprint("authBlueprint", __name__)
@authBlueprint.route("/api/v1/auth/login", methods=["POST"])
def login():
    returnUser = "SELECT * FROM users WHERE username = %s OR email = %s"
    values = (request.form['userIdentifier'],request.form['userIdentifier'])

    cursor.execute(returnUser, values)
    result = cursor.fetchone()
    
    if result is None:
        return {"result": "User not found"}
    elif bcrypt.checkpw(request.form["password"].encode("utf-8"), result[5]):
        return {"result": "Success"}
    else: 
        return {"result": "Incorrect password"}

@authBlueprint.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return {"string": "Logging out user."}