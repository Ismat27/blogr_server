from flask import jsonify, request
from .models import Post, User, db

def all_users():
    users = User.query.all()
    users = [user.format() for user in users]
    return jsonify({
        'users': users,
        'total_user': len(users),
        'success': True
    })

def single_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'message': 'user does not exist',
            'success': False
        })
    return jsonify(user.format()), 200

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'message': 'user does not exist',
            'success': False
        })
    try:
        user.delete()
        return jsonify({
            'success': True,
            'deleted_id': user_id
        })
    except Exception as error:
        db.session.rollback()
        return jsonify({
            'message': error,
            'success': False
        }), 422
    finally:
        db.session.close()

def update_user(user_id):
    user = User.query.get(user_id)
    data = request.get_json()
    if not user or not data:
        return jsonify({
            'message': 'user does not exist',
            'success': False
        }), 400
    try:
        user.insert()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            'message': error,
            'success': False
        }), 422
    finally:
        db.session.close()

def change_superuser_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'message': 'user not found',
            'success': False
        }), 400
    try:
        user.is_superuser = not user.is_superuser
        user.update()
        return jsonify(user.format())
    except Exception as error:
        return jsonify(error)

def change_admin_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'message': 'user not found',
            'success': False
        }), 400
    try:
        user.is_admin = not user.is_admin
        user.update()
        return jsonify(user.format())
    except Exception as error:
        return jsonify(error)
