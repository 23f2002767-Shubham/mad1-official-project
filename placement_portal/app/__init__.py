'''
Docstring for placement_portal.app
“Assembly room”
Bring all parts together


This is the most important file in the project, but not scary.

In simple terms, it:

Creates the Flask app

Attaches config

Attaches database (later) from extensions.py

Attaches routes (later) 
'''

'''
Python never searches all files in a package — it only executes __init__.py and looks for names defined or imported there.
'''

# app/__init__.py

from flask import Flask, app
from config import Config
from app.extensions import db, login_manager
from app.models import student  # Importing the database and login manager from extensions.py
from flask import render_template

def create_app():  # Factory function to create the Flask app
    app = Flask(__name__) # Create the Flask app instance
    #“Load all UPPERCASE variables from the Config class into the app.”
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app) # Attach the database to the app
    login_manager.init_app(app) # Attach the login manager to the app

    # Register blueprints   
    from app.blueprints.auth.routes import auth_bp # Import the auth blueprint from the auth routes file
    app.register_blueprint(auth_bp) # Register the auth blueprint with the app

    from app.blueprints.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    from app.blueprints.company.routes import company_bp
    app.register_blueprint(company_bp)

    from app.blueprints.student.routes import student_bp
    app.register_blueprint(student_bp)





    # Create tables automatically
    with app.app_context(): # Create an application context to work with the database (like one user session having one thread to work with the database)
        from app import models # Import models to ensure they are registered with SQLAlchemy
        db.create_all() # Create all tables defined in the models folder

    @app.route("/")
    def home():
        return render_template("landing.html")

    return app

