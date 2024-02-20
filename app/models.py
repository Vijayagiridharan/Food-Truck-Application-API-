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
    def insert_user(name, mobileno, emailid, password):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO userdetail (name, mobileno, emailid, passsword)
                VALUES (%s, %s, %s, %s)
            """, (name, mobileno, emailid, password))
            db.commit()
