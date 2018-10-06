from app import app_var, db
from app.models import User, Post


@app_var.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
