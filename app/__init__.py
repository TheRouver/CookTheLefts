from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Use the config dictionary to get the correct configuration class
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)

    # Add debug logging for static files
    @app.before_request
    def log_request_info():
        if app.debug:  # Only log in debug mode
            app.logger.debug('Headers: %s', request.headers)
            app.logger.debug('Body: %s', request.get_data())

    @app.after_request
    def add_header(response):
        if app.debug and request.path.startswith('/static/'):
            # Prevent caching of static files during development only
            response.headers['Cache-Control'] = 'no-store'
        elif request.path.startswith('/static/'):
            # Enable caching for static files in production
            response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response

    # Import and register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.recipes import bp as recipes_bp
    app.register_blueprint(recipes_bp, url_prefix='/recipes')

    return app

from app import models

# Create a default app instance for Gunicorn
app = create_app('production')
