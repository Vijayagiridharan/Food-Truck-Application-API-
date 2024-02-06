from . import bp

@bp.route('/')
def index():
    return "Hello from Module One!"