import sys
from . import bp
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, UserDetail
import jwt
import datetime

@bp.route('/')
def index():
    return "Hello from Module One!"

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Check if the email already exists in the database
    existing_user = UserDetail.query.filter_by(emailid=data['emailid']).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409

    # Create a new user
    new_user = UserDetail(
        name=data['name'],
        mobileno=data['mobileno'],
        emailid=data['emailid'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = UserDetail.query.filter_by(emailid=data['emailid']).first()

    if not user:
        return jsonify({"error": "Invalid email id"}), 401

    if not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Please enter correct email id/password combination"}), 401

    token = generate_jwt_token(user.userid)

    return jsonify({"token": token}), 200

def generate_jwt_token(user_id, secret_key='your-secret-key', expires_in=3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

