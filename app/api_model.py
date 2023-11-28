from flask_restx import fields
from .extentions import api



login_model = api.model('LoginModel', {
    'username': fields.String,
    'password': fields.String
})

user_model = api.model('UserModel', {
    'id': fields.Integer,
    'username': fields.String
})