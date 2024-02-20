import sys
from flask import request, jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from ..models import  UserDetail
import jwt
import datetime
from flask import Blueprint
from .. import get_db
from ..models import UserDetail
import bcrypt

login_bp = Blueprint('login', __name__, url_prefix='/auth')

@login_bp.route('/', methods=['GET'])
def index():
    return "Hello from Module One!"



@login_bp.route('/login', methods=['POST'])
def login():
    # Retrieve data sent in the request's body as JSON
    data = request.json

    # Query the UserDetail model to find a user with the provided email
    user = UserDetail.find_by_email(emailid=data['emailid'])

    # Check if the user exists in the database
    if not user:
        # If the user does not exist, return an error message
        return jsonify({"error": "Invalid email id"}), 401
    hashed_password = user['passsword']
    # Check if the provided password matches the stored hashed password
    string_password = hashed_password.decode('utf8')
    # print(user['passsword'], generate_password_hash(data['password']))
    if not check_password_hash(user['passsword'], data['password']): 
        # If the password does not match, return an error message
        return jsonify({"error": "Please enter correct email id/password combination"},user['passsword'],check_password_hash(user['passsword'], data['password']) ), 401

    # Generate a JWT token for the authenticated user
    token = generate_jwt_token(user.userid)

    # Return the generated token in the response
    return jsonify({"token": token}), 200

@login_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Check if the email already exists in the database
    existing_user = UserDetail.find_by_email(emailid=data['emailid'])
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409
    
    password = data['password']
    # Create a new user
    UserDetail.insert_user(data['name'],data['mobileno'],data['emailid'],bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()))

    return jsonify({"message": "User created successfully"}), 201



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

@login_bp.route('/test_db', methods=['GET'])
def test_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT VERSION();')
    version = cursor.fetchone()
    return {'db_version': version}
