from flask import Blueprint

bp = Blueprint('module_one', __name__, url_prefix='/module_one')

from . import routes