from flask import Flask
from app.extentions import db,api,jvt,admin
from app.models import User
from app.resources import ns



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///categories.db'
    app.config['SECRET_KEY'] = 'secret'
    app.config["JWT_SECRET_KEY"] = "secret"


    db.init_app(app)
    api.init_app(app)
    jvt.init_app(app)
    admin.init_app(app)

    api.add_namespace(ns)

    @jvt.user_identity_loader
    def user_identity_lookup(user):
        return user.id


    @jvt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).first()


    with app.app_context():
        db.create_all()
    return app