from flask import Flask, g
from dotenv import load_dotenv
import pymysql
import os


load_dotenv()

def get_db():
    if 'db' not in g:
        # Establish a database connection using configuration from .env
        g.db = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor  # Returns query results as dictionaries
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.teardown_appcontext(close_db)
    # Register Blueprints
    from .routes.routes import login_bp as login_bp
    app.register_blueprint(login_bp)



    return app

