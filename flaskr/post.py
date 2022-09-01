import uuid
from datetime import datetime
from flask import jsonify, request, abort
from .models import db, Post, User

def new_post(current_user):
    data = request.get_json()
    if not data:
        abort(400)
    try:
        title = data['title']
        content = data['content']
    except KeyError:
        abort(400)
    if not title or not content:
        abort(400)
    public_id = str(uuid.uuid4())
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

def all_posts():
    posts = Post.query.all()
    posts = [post.format() for post in posts]
    return jsonify({
        'posts': posts,
        'success': True,
        'total_posts': len(posts)
    }), 200

def single_post(post_id):
    post = Post.query.get(post_id)
    if not post:
       abort(404)
    return jsonify(post.format())

def user_posts(user_id):
    user = User.query.get(user_id)
    if not user: abort(404)
    try:
        posts = Post.query.filter_by(author_id=user_id)
        posts = [
            post.format() for
            post in posts
        ]
        return jsonify({
            'posts': posts,
            'total_posts': len(posts),
            'success': True
        })
    except Exception as error:
        abort(422)

def search_posts():
    posts = []
    if 'search_term' in request.get_json():
        search_term = request.get_json()['search_term'].strip()
        if not search_term: abort(422)
        posts = Post.query.filter(Post.title.ilike(f'%{search_term}%'))
        posts = [
            post.format() for
            post in posts
        ]
    return jsonify({
        'posts': posts,
        'total_posts': len(posts),
        'success': True
    })

def update_post(post_id):
    post = Post.query.get(post_id)
    data = request.get_json()
    if not post or not data:
        abort(404)
    try:
        title = data['title']
        content = data['content']
    except KeyError:
        abort(400)
    try:
        post.title = title
        post.content = content
        post.updated_at = datetime.now()
        post.update()
        return jsonify({
        'post': post.format(),
        'success': True
        }), 200
    except Exception as error:
        print(error)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

def remove_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    try:
        post.delete()
        return jsonify({
            'deleted_id': post_id,
            'success': True
        }), 200
    except Exception as error:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
