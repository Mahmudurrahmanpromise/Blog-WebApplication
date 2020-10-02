from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# login_manager.login_view diye bole diteci je login_required hole kon page a jete hobe.
# login_view hosche kind of redirect er moton
login_manager.login_view = "users.login"

# login page a jawar por jei flash messege ashe take customize korar jonnne aita use kora hoice
# 'info' hosche bootstrap er akta class jeta blue information alert messege show kortece aikhane
login_manager.login_message_category = 'info'
# mail
mail = Mail()


def create_app():
    app = Flask(__name__)
    # aikhane config.py file er Class ke object baniye app.config a dukiye dawa hoise.
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # aikhane import gula hosche blueprint instance
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
