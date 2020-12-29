from flask_restful import Resource
from app.models import Post
from flask import jsonify


class PostApi(Resource):
    def get(self, post_id):
        
        post = Post.query.get(post_id)
        return jsonify(post)
    
    def put(self):
        pass
    
    def post(self):
        pass
    
    def delete(self):
        pass