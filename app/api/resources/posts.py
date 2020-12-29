from flask_restful import Resource, reqparse
from app.models import Post
from flask import jsonify

parser = reqparse.RequestParser()

class PostApi(Resource):
    def get(self, post_id):
        
        post = Post.query.filter_by(id=post_id).first()
        if post:
            return jsonify({'post_id' : post.id, 'post_title' : post.title, 'post_content' : post.content})
        else:
            return 404
    
    def put(self):
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('user_id', type=int)
        args = parser.parse_args(strict=True)

        post = Post(args['title'], args['content'], args['user_id'])
        post.save()
        return 200
    
    def post(self):
        posts = User.query.all()
        
        return jsonify(posts) # need serialize
    
    def delete(self, post_id):
        post = Post.query.get(post_id)
        if post: 
            post.delete()
            return 200
        else:
            return 404