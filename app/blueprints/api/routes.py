from flask import request, jsonify

from . import bp
from app.models import Post, User
from app.blueprints.api.helpers import token_required

# Receive all posts
@bp.get('/posts')
@token_required
def api_posts(user):
    result = []
    posts = Post.query.all()
    for post in posts:
        result.append({
        'body': post.body, 
        'timestamp': post.timestamp, 
        'author': post.user_id
        })
    return jsonify(result), 200

# Receive Posts from single User
@bp.get('/posts/<username>') # <inside>is just a parameter
@token_required
def user_posts(username):
    user = User.query.filter_by(username=username).first() # left is from column comparing to right side is the parameter
    if user:
        return jsonify([{
            'body': post.body, 
            'timestamp': post.timestamp, 
            'author': post.user_id
            } for post in user.posts]), 200
    return jsonify([{'message':'Invalid Username'}]), 404    

# Send single post
@bp.get('/post/<post_id>')
@token_required
def get_post(user, post_id):
    try:
        post = Post.query.get(post_id)
        return jsonify([{
            'id': post.id,
            'body': post.body, 
            'timestamp': post.timestamp, 
            'author': post.user_id
            }])
    except:
        return jsonify([{'message':'Invalid Post Id'}]), 404    


# Make a Post
@bp.post('/post')
@token_required
def make_post(user):
    try:
        # Receive their post data
        content = request.json
        # Create a post instance or entry
        # Add foreign key to user id
        post = Post(body=content.get('body'), user_id=user.user_id)
        # commit our post 
        post.commit()
        # return message
        return jsonify([{'message': 'Post Created', 'body':post.body}]), 200
    except:
        jsonify([{'message':'invalid form data'}]), 401