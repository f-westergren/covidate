from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'index.index'
login.login_message_category = "danger"

def create_app():
  """Create Flask Application."""

  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///covid'
  app.config.from_object('config.Config')
  
  db.init_app(app)
  login.init_app(app)

  with app.app_context():
    # Import parts of our application
    from .index import index
    from .auth import auth
    from .search import search

    # Register Blueprints
    app.register_blueprint(index.index_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(search.search_bp)

    return app