# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# # Creating table: userdetails that will store information about user
# class UserDetail(db.Model):
#     __tablename__ = 'userdetail'

#     userid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(45), nullable=False)
#     mobileno = db.Column(db.String(45), nullable=False)
#     emailid = db.Column(db.String(45), unique=True, nullable=False)
#     password = db.Column(db.String(45), nullable=False)
from . import get_db

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
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO userdetail (name, mobileno, emailid, passsword,isAdmin)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, mobileno, emailid, password, isAdmin))
            db.commit()



# class Item:
#     @staticmethod
#     def insert_item(name, pictureUrl, price, description):
#         db = get_db()
#         with db.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO item (name, pictureUrl, price, description)
#                 VALUES (%s, %s, %s, %s)
#             """, (name, pictureUrl, price, description))
#             db.commit()

#     @staticmethod
#     def get_item(itemId):
#         db = get_db()
#         with db.cursor() as cursor:
#             cursor.execute("""
#                 SELECT * FROM item WHERE itemId = %s
#             """, (itemId,))
#             return cursor.fetchone()

#     @staticmethod
#     def update_item(itemId, name, pictureUrl, price, description):
#         db = get_db()
#         with db.cursor() as cursor:
#             cursor.execute("""
#                 UPDATE item SET name = %s, pictureUrl = %s, price = %s, description = %s WHERE itemId = %s
#             """, (name, pictureUrl, price, description, itemId))
#             db.commit()

#     @staticmethod
#     def delete_item(itemId):
#         db = get_db()
#         with db.cursor() as cursor:
#             cursor.execute("""
#                 DELETE FROM item WHERE itemId = %s
#             """, (itemId,))
#             db.commit()



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