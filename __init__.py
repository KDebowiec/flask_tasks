from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import timedelta
from flask_marshmallow import Marshmallow, fields

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    encryptor = md5()

    app.permanent_session_lifetime = timedelta(minutes=30)
    app.secret_key = encryptor.digest()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)
    ma.init_app(app)

    app.debug = True

    from .main import login_blueprint, dashboard_blueprint, logout_blueprint, add_note_blueprint, get_note_blueprint,\
        get_notes_blueprint, update_note_blueprint, delete_note_blueprint, adding_note_blueprint, add_note_from_form_blueprint

    app.register_blueprint(login_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(logout_blueprint)
    # app.register_blueprint(add_note_blueprint)
    app.register_blueprint(get_notes_blueprint)
    app.register_blueprint(get_note_blueprint)
    app.register_blueprint(update_note_blueprint)
    app.register_blueprint(delete_note_blueprint)
    # app.register_blueprint(adding_note_blueprint)
    app.register_blueprint(add_note_from_form_blueprint)

    return app
