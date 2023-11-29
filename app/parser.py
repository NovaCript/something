from flask_restx import reqparse

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1, help='Page number')
parser.add_argument('per_page', type=int, default=10, help='Items per page')
