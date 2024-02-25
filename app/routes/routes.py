import sys
from flask import jsonify, Blueprint, request
#from werkzeug.security import check_password_hash,generate_password_hash
from ..models import  UserDetail, Item
import jwt
import datetime
from flask import Blueprint
from .. import get_db
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

    if (data['password']==user['passsword']): 
        if(data['isAdmin']==user['isAdmin']):
            return jsonify({"success": "Login successful"}),201
        else:
            return jsonify({"error": "User doesnt have admin credentials and cant enter admin module"}),201    
    else:
        # If the password does not match, return an error message
        return jsonify({"error": "Please enter correct email id/password combination"}), 401

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
    
    
    # Create a new user
    UserDetail.insert_user(data['name'],data['mobileno'],data['emailid'],data['password'],data['isAdmin'])

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





item_bp = Blueprint('item', __name__, url_prefix='/item')

@item_bp.route('/create', methods=['POST'])
def create_item():
    """
    API endpoint to create a new item.
    Expects a JSON payload with name, pictureUrl, price, and description.

    Returns:
        A JSON response with a success message and a 201 HTTP status code if the item is created successfully.
    """
    data = request.json
    Item.insert_item(data['name'], data['pictureUrl'], data['price'], data['description'])
    return jsonify({"message": "Item created successfully"}), 201




@item_bp.route('/<int:item_id>', methods=['GET'])
def read_item(item_id):
    """
    API endpoint to retrieve an item by its ID.

    Args:
        item_id (int): Unique identifier of the item.

    Returns:
        A JSON response with the item data and a 200 HTTP status code if the item is found.
        If the item is not found, returns a JSON error message with a 404 HTTP status code.
    """
    item = Item.get_item(item_id)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404




@item_bp.route('/update/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    API endpoint to update an existing item.

    Args:
        item_id (int): Unique identifier of the item to update.
    
    Expects a JSON payload with updated name, pictureUrl, price, and description.

    Returns:
        A JSON response with a success message and a 200 HTTP status code if the update is successful.
    """
    data = request.json
    Item.update_item(item_id, data['name'], data['pictureUrl'], data['price'], data['description'])
    return jsonify({"message": "Item updated successfully"}), 200




@item_bp.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    API endpoint to delete an item by its ID.

    Args:
        item_id (int): Unique identifier of the item to delete.

    Returns:
        A JSON response with a success message and a 200 HTTP status code if the deletion is successful.
    """
    Item.delete_item(item_id)
    return jsonify({"message": "Item deleted successfully"}), 200



@item_bp.route('/all', methods=['GET'])
def get_all_items():
    """API endpoint to get all items.

    Returns:
        A JSON response with a list of all items and a 200 HTTP status code.
    """
    items = Item.get_all_items()  # Assuming get_all_items is the method to fetch all items
    return jsonify(items), 200

