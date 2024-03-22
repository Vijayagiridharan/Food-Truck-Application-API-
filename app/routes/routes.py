import sys
from flask import jsonify, Blueprint, request
#from werkzeug.security import check_password_hash,generate_password_hash
from ..models import  UserDetail, Item,orderdetail,orderitemdetails
import jwt
import datetime
from flask import Blueprint
from .. import get_db
import csv
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
from google.cloud import storage
from io import StringIO


gcs_client = storage.Client()

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
order_bp = Blueprint ('order', __name__, url_prefix='/order')

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

@order_bp.route('/create', methods=['POST'])
def create_order():
    """
    API endpoint to create a new item.
    Expects a JSON payload with name, pictureUrl, price, and description.

    Returns:
        A JSON response with a success message and a 201 HTTP status code if the item is created successfully.
    """
    data = request.json
    orderdetail.insert_order(data['username'], data['orderstatus'], data['paymentstatus'], data['totalprice'])
    
    orderid = orderdetail.get_last_inserted_order_id()
    
    # Insert items into the orderitemdetails table
    for item in data['items']:
        orderitemdetails.insert_orderitem(orderid, item['itemid'], item['itemquantity'], item['itemprice'], item['itemdescription'])
    
    
    """orderitemdetails.insert_orderitem(data['orderid'], data['itemid'], data['itemquantity'], data['itemprice'], data['itemdescription'])"""
    return jsonify({"message": "Order created successfully"}), 201

@order_bp.route('/getordersuccess', methods=['GET'])
def get_accepted_orders_with_items():
    """
    API endpoint to fetch all order details with order status "Accepted" and payment status "Success"
    along with their corresponding item details.

    Returns:
        A JSON response with a list of order details and their corresponding item details and a 200 HTTP status code.
    """
    db = get_db()
    accepted_orders_with_items = {}
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT od.username, od.orderid, od.orderstatus, od.paymentstatus, od.totalprice,
                   oid.itemid, oid.itemquantity, oid.itemprice, oid.itemdescription
            FROM orderdetail od
            JOIN orderitemdetails oid ON od.orderid = oid.orderid
            WHERE od.orderstatus = 'I' AND od.paymentstatus = 'S'
        """)
        orders = cursor.fetchall()
        for order in orders:
            username = order['username']
            order_id = order['orderid']
            if username not in accepted_orders_with_items:
                accepted_orders_with_items[username] = {
                    'username': username,
                    'orderid': order_id,
                    'orderstatus': order['orderstatus'],
                    'paymentstatus': order['paymentstatus'],
                    'totalprice': order['totalprice'],
                    'items': []
                }
            accepted_orders_with_items[username]['items'].append({
                'itemid': order['itemid'],
                'itemquantity': order['itemquantity'],
                'itemprice': order['itemprice'],
                'itemdescription': order['itemdescription']
            })

    # Convert dictionary values to list
    accepted_orders_with_items_list = list(accepted_orders_with_items.values())

    return jsonify(accepted_orders_with_items_list), 200

@order_bp.route('/update/<int:orderid>', methods=['PUT'])
def update_order(orderid):
    """
    API endpoint to update an existing order.

    Args:
        orderid (int): Unique identifier of the order to update.
    
    Expects a JSON payload with updated order status.

    Returns:
        A JSON response with a success message and a 200 HTTP status code if the update is successful,
        otherwise, returns an error message with a 400 HTTP status code.
    """
    data = request.json

    # Check if the orderid exists
    existing_order = orderdetail.find_order_by_id(orderid)
    if not existing_order:
        return jsonify({"error": f"Order with id {orderid} does not exist"}), 404

    # Update the order in the database
    orderdetail.update_order(orderid,data['orderstatus'])
    return jsonify({"message": "Order updated successfully"}), 200

@order_bp.route('/<int:orderid>', methods=['GET'])
def read_order(orderid):
    """
    API endpoint to retrieve an item by its ID.

    Args:
        item_id (int): Unique identifier of the item.

    Returns:
        A JSON response with the item data and a 200 HTTP status code if the item is found.
        If the item is not found, returns a JSON error message with a 404 HTTP status code.
    """
    orderstatus = orderdetail.getorderstatus(orderid)
    if orderstatus:
        return jsonify(orderstatus), 200
    else:
        return jsonify({"error": "order id not found"}), 404



@item_bp.route('/csv', methods=['POST'])
def upload_csv():
    """
    Route to upload a CSV file and process it to add items to the database.
    The CSV should have item details in the following order:
    itemId, name, pictureUrl, price, description.
    Duplicates are checked against the `itemId`.

    :return: A string response indicating the result of the upload and processing.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        try:
            bucket_name = 'food_truck_csv'  # Replace with your actual bucket name
            bucket = gcs_client.get_bucket(bucket_name)
            filename = secure_filename(file.filename)
            blob = bucket.blob(filename)
            blob.upload_from_string(file.read(), content_type='text/csv')
            # At this point, the file is uploaded to Google Cloud Storage
            # Now, you may proceed to process the file as needed
            csv_content = blob.download_as_text()
            csv_reader = csv.reader(StringIO(csv_content))
            next(csv_reader)  # Skip the header row if present
        
        # Process CSV data
            for row in csv_reader:
                name, picture_url, price, description,item_id = row
                # Check if an item with the same itemId already exists to avoid duplicates
                print()
                if not Item.get_item(itemId=int(item_id)):
                    Item.insert_item(name, picture_url, float(price), description)
                else:  # If an item with the same itemId exists, update it
                    Item.update_item(int(item_id), name, picture_url, float(price), description)
            return 'File uploaded and processed successfully to GCS', 200
        except Exception as e:
            return jsonify({'error': 'Failed to process file', 'message': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


        

