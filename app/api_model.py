from flask_restx import fields
from .extentions import api



login_model = api.model('Login', {
    'username': fields.String,
    'password': fields.String
})

user_model = api.model('User', {
    'id': fields.Integer,
    'username': fields.String
})


product_model = api.model('Product',{
    'id':fields.Integer,
    'name': fields.String,
    'image_small':fields.String,
    'image_medium':fields.String,
    'image_large':fields.String,
    'price': fields.Integer,
    'subcategory_id': fields.Integer,
    'subcategory.category_id':fields.Integer
})

subcategory_model = api.model('Subcategory', {
    'id': fields.Integer,
    'name': fields.String,
    'slug_name': fields.String,
    'image_url': fields.String,
    'category_id': fields.Integer
})

category_model = api.model('Category', {
    'id':fields.Integer,
    'name':fields.String,
    'slug_name': fields.String,
    'image_large': fields.String,
    'subcategories':fields.List(fields.Nested(subcategory_model))

})

