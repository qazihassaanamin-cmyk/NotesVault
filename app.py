import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db, User

# Initialize Flask application
app = Flask(__name__)

# Basic Application Configuration
app.config['SECRET_KEY'] = 'notesvault-secret-key-2026-super-secure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notesvault.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy database instance to Flask app
db.init_app(app)

# Initialize Flask-Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Callback to reload user object from session user_id."""
    return User.query.get(int(user_id))

# Import and Register Blueprints
from routes.auth import auth as auth_blueprint
from routes.resources import resources as resources_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(resources_blueprint)

# Root route redirecting to marketplace
@app.route('/')
def home():
    return redirect(url_for('resources.marketplace'))

# Application Execution Entry Point
if __name__ == '__main__':
    with app.app_context():
        # Auto-create database tables locally if they don't exist
        db.create_all()
    app.run(debug=True)