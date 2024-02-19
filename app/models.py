from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Creating table: userdetails that will store information about user
class UserDetail(db.Model):
    __tablename__ = 'userdetail'

    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    mobileno = db.Column(db.String(45), nullable=False)
    emailid = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)

