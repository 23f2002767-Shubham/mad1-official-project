from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLAlchemy database instance
db = SQLAlchemy()

# Flask-Login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login_view" #If someone tries: /dashboard without logging in, they will be redirected to /auth/login
# auth is the name of the blueprint, login is the name of the function in auth/routes.py that handles the login page

# Flask-Login requires this to reload user from session
@login_manager.user_loader #This decorator tells Flask-Login that this function will be used to load a user given their ID. When a user logs in, their ID is stored in the session. For subsequent requests, Flask-Login will call this function with the stored user ID to retrieve the user object from the database.
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))