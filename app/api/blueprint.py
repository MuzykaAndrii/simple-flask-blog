from flask import Blueprint, redirect, url_for
from flask_restful import Api
from app.api.resources.posts import PostApi

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

@api_bp.route('/')
def api_redirect():
    return redirect(url_for('index'))

api.add_resource(PostApi, '/post/<int:post_id>', '/post', '/post/<int:post_id>/delete', '/posts')