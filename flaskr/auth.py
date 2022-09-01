from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from flask import request, jsonify, abort
from .models import User
import jwt
from functools import wraps
from .models import Post

def is_superuser(current_user):
    return current_user.is_superuser

def sign_up_user():
    data = request.get_json()
    if not data:
        return jsonify({
            'message': 'no user data',
            'success': False
        }), 400
    print(data)
    try:
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
    except KeyError:
        return jsonify({
            'message': 'missing data',
            'success': False
        })

    if not first_name or not last_name or not email or not password:
        return jsonify({
            'message': 'missing data',
            'success': False
        })
    user = User.query.filter_by(email=email).first()
    if user:
       return jsonify({
            'message': 'user already existing pls log in',
            'success': False
        }), 400
    try:
        user = User(
            public_id = str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password)
        )
        user.insert()
        return jsonify({
            'success': True,
            'created_user': user.format()
        }), 201
    except Exception as error:
        print(error)
        return jsonify({
            'success': False,
            'message': 'unable to process request'
        }),422

def login_in_user():
    data = request.get_json()
    if not data:
        return jsonify({
            "message": "user details not provided",
            "error": "Bad request",
            'success': False
        }), 400
    
    try:
        email = data['email']
        password = data['password']
    except KeyError:
        return jsonify({
            'message': 'missing data',
            'success': False
        }), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            'message': 'incorrect credentials',
            'success': False
        }), 404
    if check_password_hash(user.password, password):
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(days=7),
            }, 'thisisthesecretkey', algorithm='HS256'
        )
        return jsonify({
            'success': True,
            'token': token,
            'user': user.format()
        }), 200

    return jsonify({
        'message': 'incorrect credentials',
        'success': False
    }), 422

def get_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            abort(401)
        try:
            data = jwt.decode(token, 'thisisthesecretkey', algorithms=['HS256'])
            current_user = User.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except Exception as error:
            print(error)
            abort(401)
        return f(current_user, *args, **kwargs)
    return decorated

def authorize(current_user, post_id):
    def authorize_(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            post = Post.query.get(post_id)
            if not post:
                return jsonify({
                    'message': 'resource not found',
                    'success': False
                }), 403
            is_admin = current_user.is_admin
            is_superuser = current_user.is_superuser
            if is_superuser:
                return f(current_user, *args, **kwargs)
            elif (is_admin and post.author_id == current_user.id):
                return f(current_user, *args, **kwargs)
            return jsonify({
                'message': 'not authorize',
                'success': False
            }), 405
        return wrapper
    return authorize_

def allow_update_post(current_user, post_id):
    post = Post.query.get(post_id)
    if not post: abort(404)
    is_superuser = current_user.is_superuser
    if is_superuser: return True
    is_admin = current_user.is_admin
    if (is_admin and post.author_id == current_user.id):
        return True
    return False

def allow_update_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user: return False
    is_superuser = current_user.is_superuser
    if is_superuser: return True
    is_admin = current_user.is_admin
    if (is_admin and current_user.id == user_id):
        return True
    return False