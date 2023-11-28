from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restx import Api, Namespace, fields, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, \
    create_access_token, current_user, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///categories.db'
app.config['SECRET_KEY'] = 'secret'
app.config["JWT_SECRET_KEY"] = "secret"
api = Api(app)
db = SQLAlchemy(app)
admin = Admin(app)
jvt = JWTManager(app)


authorizations = {
    'jsonWebToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


ns = Namespace('shop/', authorizations=authorizations)

api.add_namespace(ns)


@jvt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jvt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(100))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug_name = db.Column(db.String(100), unique=True)
    image_url = db.Column(db.String(255))
    subcategories = db.relationship('Subcategory', back_populates='category')

    def __repr__(self):
        return self.name


class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug_name = db.Column(db.String(100), unique=True)
    image_url = db.Column(db.String(255))
    category_id = db.Column(db.ForeignKey('category.id'), nullable=False)

    category = db.relationship("Category", back_populates='subcategories')
    product = db.relationship('Products', back_populates='subcategory')

    def __repr__(self):
        return self.name


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug_name = db.Column(db.String(100), unique=True)
    image_small = db.Column(db.String(255))
    image_medium = db.Column(db.String(255))
    image_large = db.Column(db.String(255))
    price = db.Column(db.Integer)
    subcategory_id = db.Column(db.ForeignKey('subcategory.id'), nullable=False)

    subcategory = db.relationship('Subcategory', back_populates='product')

    def __repr__(self):
        return self.name


class SubcategoryPost(ModelView):
    form_columns = ['name', 'slug_name', 'image_url', 'category']
    column_list = ['name', 'slug_name', 'image_url', 'category']


class ProductPost(ModelView):
    form_columns = ['name', 'slug_name', 'image_small', 'image_medium',
                    'image_large', 'price', 'subcategory']
    column_list = ['name', 'slug_name', 'image_small', 'image_medium',
                   'image_large', 'price', 'subcategory']


admin.add_views(ModelView(Category, db.session),
                SubcategoryPost(Subcategory, db.session),
                ProductPost(Products, db.session))

login_model = api.model('LoginModel', {
    'username': fields.String,
    'password': fields.String
})

user_model = api.model('UserModel', {
    'id': fields.Integer,
    'username': fields.String
})


@ns.route("/hello")
class Hello(Resource):
    method_decorators = [jwt_required()]
    @ns.doc(security='jsonWebToken')
    def get(self):
        uid = get_jwt_identity()
        return {'self.uid': uid}

@ns.route("/register")
class Register(Resource):

    @ns.expect(login_model)
    @ns.marshal_with(user_model)
    def post(self):
        user = User(username=ns.payload['username'],
                    password_hash=generate_password_hash(
                        ns.payload['password']))
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=ns.payload['username']).first()
        if not user:
            return {'error':'User does not exist'}, 401
        if not check_password_hash(user.password_hash, ns.payload['password']):
            return {'error':'Incorrect password'}, 401
        return {'access_token': create_access_token(user)}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
