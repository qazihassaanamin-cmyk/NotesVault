import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User, Category
from routes.auth import auth_bp
from routes.resources import resources_bp
from routes.search import search_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(search_bp)

    @app.route('/')
    def root():
        return redirect(url_for('resources.dashboard'))

    with app.app_context():
        db.create_all()
        # Seed initial categories if empty
        if not Category.query.first():
            default_categories = [
                Category(name='Calculus', description='Calculus I, II, Limits, Differentiation'),
                Category(name='Physics', description='Mechanics, Electricity, Magnetism'),
                Category(name='Python', description='Core Python, Flask, Algorithms'),
                Category(name='SQL', description='Database Queries, Relational Schemas')
            ]
            db.session.bulk_save_objects(default_categories)
            db.session.commit()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)