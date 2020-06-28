from app import app, db
from app.models import User, Search

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Search': Search}