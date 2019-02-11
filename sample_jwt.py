# Author: Sebastian Ma <sebmalikkeung@gmail.com>
# Description: 
# A basic JWT program, refer to https://flask-jwt-extended.readthedocs.io/en/latest/
# Tested with curl on Linux. Tested with postman on Windows.
# On Windows, remember to use %YOUR_ENV_NAME% instead of $YOUR_ENV_NAME.
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    print("Entering login()")
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    print(username)
    print(password)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# No jwt_required for this route
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"msg": "Guten Tag!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(host="0.0.0.0")

