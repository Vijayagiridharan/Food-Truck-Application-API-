from flask import Blueprint

bp = Blueprint('module_one', __name__, url_prefix='/module_one')


def create_app():
    app = Flask(__name__)
    from app.module_one import routes  
    app.register_blueprint(bp)
    return app
