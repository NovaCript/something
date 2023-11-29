from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity, \
    create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from .parser import parser
from .models import User, Products, Subcategory, Category
from .api_model import login_model, user_model, product_model, \
    subcategory_model, category_model
from .extentions import db

authorizations = {
    'jsonWebToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

ns = Namespace('shop/', authorizations=authorizations)


@ns.route("/hello")
class Hello(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security='jsonWebToken')
    def get(self):
        uid = get_jwt_identity()
        return {'Hello user': uid}


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
            return {'error': 'User does not exist'}, 401
        if not check_password_hash(user.password_hash, ns.payload['password']):
            return {'error': 'Incorrect password'}, 401
        return {'access_token': create_access_token(user)}


@ns.route('/product')
class ProductListAPI(Resource):

    @ns.expect(parser)
    @ns.marshal_list_with(product_model)
    def get(self):
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        product = Products.get_paginate(page, per_page)

        return product.items, 200


@ns.route('/subcategory')
class SubCategoryAPI(Resource):

    @ns.expect(parser)
    @ns.marshal_list_with(subcategory_model)
    def get(self):
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        product = Subcategory.get_paginate(page, per_page)

        return product.items, 200


@ns.route('/category')
class CategoryListApi(Resource):

    @ns.expect(parser)
    @ns.marshal_list_with(category_model)
    def get(self):
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        product = Category.get_paginate(page, per_page)

        return product.items, 200
