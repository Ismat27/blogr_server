from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from .models import setup_db
from .post import \
    all_posts, new_post, remove_post, single_post, \
    update_post, user_posts, search_posts
from .auth import \
    is_superuser, sign_up_user,login_in_user, get_token, allow_update_post
from .user import \
    all_users, single_user, delete_user, update_user,\
    change_admin_status, change_superuser_status


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def hello():
        return jsonify('You are welcome to Blogr')

    @app.route('/signup', methods=['POST'])
    def signup():
        return sign_up_user()

    @app.route('/login', methods=['POST'])
    def login():
        return login_in_user()

    @app.route('/users')
    @get_token
    def get_all_users(current_user):
        if is_superuser(current_user):
            return all_users()
        else: abort(403)
    
    @app.route('/users/<int:user_id>', methods=['GET'])
    @get_token
    def get_single_user(current_user, user_id):
        if is_superuser(current_user):
            return single_user(user_id)
        else: abort(403)

    @app.route('/users/<int:user_id>', methods=['DELETE', 'PUT'])
    @get_token
    def delete_update_user(current_user, user_id):
        if not is_superuser(current_user):
            abort(403)
        if request.method == 'DELETE':
            return delete_user(user_id)
        if request.method == 'PUT':
            return update_user(user_id)

    @app.route('/change_superstatus/<int:user_id>', methods=['PATCH'])
    @get_token
    def change_superstatus(current_user, user_id):
        if not is_superuser(current_user):
            abort(403)
        return change_superuser_status(user_id)
    
    @app.route('/change_adminstatus/<int:user_id>', methods=['PATCH'])
    @get_token
    def change_adminstatus(current_user, user_id):
        if not is_superuser(current_user):
            abort(403)
        return change_admin_status(user_id)

    @app.route('/posts', methods=['POST'])
    @get_token
    def make_new_post(current_user):
        return new_post(current_user)
    
    @app.route('/posts')
    def get_all_posts():
        return all_posts()
    
    @app.route('/posts/<int:post_id>', methods=['GET'])
    def one_post(post_id):
        return single_post(post_id)
    
    @app.route('/users/<int:user_id>/posts', methods=['GET'])
    def posts_by_user(user_id):
        return user_posts(user_id)

    @app.route('/posts/search', methods=['POST'])
    def posts_by_search():
        return search_posts()
    
    @app.route('/posts/<int:post_id>', methods=['PUT', 'DELETE'])
    @get_token
    def delete_update_post(current_user, post_id):
        if not allow_update_post(current_user=current_user, post_id=post_id):
            abort(403)
        if request.method == 'PUT':
            return update_post(post_id)
        if request.method == 'DELETE':
            return remove_post(post_id)
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad Request',
            'status_code': 400
        }), 400

    @app.errorhandler(401)
    def user_unknown(error):
        return jsonify({
            'success': False,
            'message': 'sender not authenticated',
            'status_code': 401
        }), 401
    
    @app.errorhandler(403)
    def acess_denied(error):
        return jsonify({
            'success': False,
            'message': 'access denied',
            'status_code': 403
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'resource not found',
            'status_code': 404
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'method not allowed',
            'status_code': 405
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': 'request is unprocessable',
            'status_code': 422
        }), 422

    return app
