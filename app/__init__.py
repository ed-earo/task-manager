from flask import Flask

from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "change-this-later"

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from app import models

    with app.app_context():
        db.create_all()

    from app.auth import auth
    from app.tasks import tasks

    app.register_blueprint(auth)
    app.register_blueprint(tasks)

    return app