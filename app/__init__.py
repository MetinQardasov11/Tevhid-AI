from flask import Blueprint

app_bp = Blueprint('app', __name__, url_prefix='/', template_folder='templates', static_folder='static/uploads', static_url_path='/static/uploads')


from . import routes