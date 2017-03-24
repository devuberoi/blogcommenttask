from flask import Blueprint, request
from werkzeug.datastructures import CombinedMultiDict
from tools.Toolkit import respond
from view import create_blog, get_blog, list_blogs, create_comment

api = Blueprint('blogs', __name__, url_prefix='/blogs')

@api.route('/', methods=['POST'])
def post_one():
    parameters = request.get_json()
    response = create_blog(parameters)
    return respond(response)

@api.route('/', methods=['GET'])
def get_all():
    parameters = CombinedMultiDict([request.args, request.form])
    response = list_blogs(parameters)
    return respond(response)

@api.route('/<blog_id>', methods=['GET'])
def get_single(blog_id):
    parameters = CombinedMultiDict([request.args, request.form])
    response = get_blog(parameters, blog_id)
    return respond(response)

@api.route('/<blog_id>/comment', methods=['POST'])
def post_comment(blog_id):
    parameters = request.get_json()
    response = create_comment(parameters, blog_id)
    return respond(response)
