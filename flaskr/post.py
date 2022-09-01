import json
import uuid
from datetime import datetime
from flask import jsonify, request, abort
from .models import db, Post, User

def all_posts():
    posts = Post.query.all()
    posts = [post.format() for post in posts]
    return jsonify({
        'posts': posts,
        'success': True,
        'total_posts': len(posts)
    }), 200

def new_post(current_user):
    data = request.get_json()
    if not data:
        return jsonify({
            'message': 'post data not included',
            'success': False
        }), 400
    try:
        title = data['title']
        content = data['content']
    except KeyError:
        return jsonify({
            'message': 'bad request',
            'success': False,
        }), 400
    public_id = str(uuid.uuid4())
    if not title or not content:
        return jsonify({
            'message': 'bad request',
            'success': False,
        }), 400
    try:
        post = Post(
            public_id=public_id,
            title=title,
            content=content,
            author_id=current_user.id,
            author=current_user
        )
        post.insert()
        return jsonify({
            'success': True,
            'post': post.format()
        }), 200
    except Exception as error:
        return jsonify({
            'message': 'unable to complete request',
            'success': False,
        }), 422

def remove_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({
            'message': 'resource not found',
            'success': True
        }), 404
    
    return jsonify({
        'message': 'Delete possible',
        'success': True
    })
    
    # try:
    #     post.delete()
    # except Exception as error:
    #     db.session.rollback()
    # finally:
    #     db.session.close()
def single_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({
            'message': 'resource not found',
            'success': False
        }), 404
    return jsonify(post.format())

def update_post(post_id):
    post = Post.query.get(post_id)
    data = request.get_json()
    if not post or not data:
        return jsonify({
            'message': 'resource not found',
            'success': True
        }), 404
    try:
        title = data['title']
        content = data['content']
    except KeyError:
        return jsonify({
            'success': False,
            'message': 'missing data'
        }), 400
    try:
        post.title = title
        post.content = content
        post.updated_at = datetime.now()
        post.update()
        return jsonify({
        'post': post,
        'success': True
        }), 200
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({
            'message': 'update failed',
            'success': False
        }), 422
    finally:
        db.session.close()
    