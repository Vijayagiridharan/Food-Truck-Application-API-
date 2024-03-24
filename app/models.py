from . import get_db
import bcrypt
import hashlib

class UserDetail:
    @staticmethod
    def find_by_email(emailid):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM userdetail WHERE emailid = %s
            """, (emailid,))
            return cursor.fetchone()

    @staticmethod
    def insert_user(name, mobileno, emailid, password,isAdmin):
        db = get_db()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO userdetail (name, mobileno, emailid, passsword,isAdmin)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, mobileno, emailid, hashed_password, isAdmin))
            db.commit()

    @staticmethod
    def validate_password(user, emailid, input_password):
       hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
      
       
       if user and hashed_input_password == user['passsword']:
            print("Passwords match!")  # Debugging print
            return True  # Password matches
       else:
            print("Passwords do not match!")  # Debugging print
            return False  # Password does not match



class orderdetail:
    """
    Represents an item entity with operations to interact with the database.
    This class provides static methods to insert, retrieve, update, and delete items in the database.
    """

    @staticmethod
    def insert_order(username, orderstatus, paymentstatus, totalprice):
        """
        Inserts a new item into the database.

        Args:
            name (str): The name of the item.
            pictureUrl (str): The URL of the picture associated with the item.
            price (float): The price of the item.
            description (str): The description of the item.

        Commits the new item to the database.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO orderdetail (username, orderstatus, paymentstatus, totalprice)
                VALUES (%s, %s, %s, %s)
            """, (username, orderstatus, paymentstatus, totalprice))
            db.commit()

    @staticmethod
    def get_last_inserted_order_id():
        """
        Retrieves the ID of the last inserted order from the database.

        Returns:
            int: The ID of the last inserted order.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT orderid FROM orderdetail ORDER BY orderid DESC LIMIT 1
            """)
            last_order = cursor.fetchone()
            if last_order:
                return last_order['orderid']
            else:
                # Handle the case when no order is found in the database
                return None
            
    @staticmethod
    def find_order_by_id(orderid):
        """
        Retrieves an order from the database by its ID.

        Args:
            orderid (int): The unique identifier of the order.

        Returns:
            dict: A dictionary containing the order data if found, otherwise None.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM orderdetail WHERE orderid = %s
            """, (orderid,))
            return cursor.fetchone()
        
    @staticmethod
    def update_order(orderid,orderstatus):
        """
        Updates an existing item in the database.

        Args:
            itemId (int): The unique identifier of the item to be updated.
            name (str): The new name for the item.
            pictureUrl (str): The new picture URL for the item.
            price (float): The new price for the item.
            description (str): The new description for the item.

        Commits the updates to the database.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE orderdetail SET orderstatus = %s WHERE orderid = %s
            """, (orderstatus,orderid))
            db.commit()

    @staticmethod
    def getorderstatus(orderid):
        """
        Retrieves an item from the database by its ID.

        Args:
            itemId (int): The unique identifier of the item.

        Returns:
            dict: A dictionary containing the item data if found, otherwise None.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT orderstatus FROM orderdetail WHERE orderid = %s
            """, (orderid,))
            return cursor.fetchone()

class orderitemdetails:
    """
    Represents an item entity with operations to interact with the database.
    This class provides static methods to insert, retrieve, update, and delete items in the database.
    """

    @staticmethod
    def insert_orderitem(orderid, itemid, itemquantity, itemprice, itemdescription):
        """
        Inserts a new item into the database.

        Args:
            name (str): The name of the item.
            pictureUrl (str): The URL of the picture associated with the item.
            price (float): The price of the item.
            description (str): The description of the item.

        Commits the new item to the database.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO orderitemdetails (orderid, itemid, itemquantity, itemprice, itemdescription)
                VALUES (%s, %s, %s, %s, %s)
            """, (orderid, itemid, itemquantity, itemprice, itemdescription))
            db.commit()

class Item:
    """
    Represents an item entity with operations to interact with the database.
    This class provides static methods to insert, retrieve, update, and delete items in the database.
    """

    @staticmethod
    def insert_item(name, pictureUrl, price, description):
        """
        Inserts a new item into the database.

        Args:
            name (str): The name of the item.
            pictureUrl (str): The URL of the picture associated with the item.
            price (float): The price of the item.
            description (str): The description of the item.

        Commits the new item to the database.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO item (name, pictureUrl, price, description)
                VALUES (%s, %s, %s, %s)
            """, (name, pictureUrl, price, description))
            db.commit()



    @staticmethod
    def get_item(itemId):
        """
        Retrieves an item from the database by its ID.

        Args:
            itemId (int): The unique identifier of the item.

        Returns:
            dict: A dictionary containing the item data if found, otherwise None.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM item WHERE itemId = %s
            """, (itemId,))
            return cursor.fetchone()



    @staticmethod
    def update_item(itemId, name, pictureUrl, price, description):
        """
        Updates an existing item in the database.

        Args:
            itemId (int): The unique identifier of the item to be updated.
            name (str): The new name for the item.
            pictureUrl (str): The new picture URL for the item.
            price (float): The new price for the item.
            description (str): The new description for the item.

        Commits the updates to the database.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE item SET name = %s, pictureUrl = %s, price = %s, description = %s WHERE itemId = %s
            """, (name, pictureUrl, price, description, itemId))
            db.commit()




    @staticmethod
    def delete_item(itemId):
        """
        Deletes an item from the database by its ID.

        Args:
            itemId (int): The unique identifier of the item to be deleted.

        Commits the deletion to the database.
        """
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                DELETE FROM item WHERE itemId = %s
            """, (itemId,))
            db.commit()




    @staticmethod
    def get_all_items():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM item
            """)
            return cursor.fetchall()
        
