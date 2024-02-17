import sys
from . import bp
from flask import request, jsonify
from werkzeug.security import check_password_hash
from models import db, UserDetail
import jwt
import datetime
from ..models import db, UserDetail

@bp.route('/')
def index():
    return "Hello from Module One!"



@bp.route('/login', methods=['POST'])
def login():
    # Retrieve data sent in the request's body as JSON
    data = request.json

    # Query the UserDetail model to find a user with the provided email
    user = UserDetail.query.filter_by(emailid=data['emailid']).first()

    # Check if the user exists in the database
    if not user:
        # If the user does not exist, return an error message
        return jsonify({"error": "Invalid email id"}), 401

    # Check if the provided password matches the stored hashed password
    if not check_password_hash(user.password, data['password']):
        # If the password does not match, return an error message
        return jsonify({"error": "Please enter correct email id/password combination"}), 401

    # Generate a JWT token for the authenticated user
    token = generate_jwt_token(user.userid)

    # Return the generated token in the response
    return jsonify({"token": token}), 200



def generate_jwt_token(user_id, secret_key='your-secret-key', expires_in=3600):
    """
    Generates a JWT token.

    :param user_id: The user's identifier (e.g., user ID from the database)
    :param secret_key: The secret key used to encode the JWT
    :param expires_in: The duration in seconds for which the token is valid
    :return: A JWT token as a string
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')