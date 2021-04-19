from flask import Blueprint, request, jsonify
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter
from core.utilities.functions import get_limit
from core.database.repository.users import UserRepository

api_users = Blueprint('api_users', __name__)

@api_users.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def users():
    limit = get_limit(api_users)

    if limit > 100:
        limit = 100

    rows = UserRepository().getAll([limit])

    return jsonify(list(map(lambda row: {
        'id': row['id'],
        'tg_id': row['tg_id'],
        'username': row['tg_username'],
        'warn': row['warn_count'],
    }, rows)))

@api_users.route('/users/<int:tg_id>', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def user(tg_id):
    row = UserRepository().getById([tg_id])
    if row:
        return {'id': row['id'],
        'tg_id': row['tg_id'],
        'username': row['tg_username'],
        'warn': row['warn_count']}
    else:
        return {'error': 'You have entered an id that does not exist or you have entered incorrect data'}

@api_users.route('/users/delete_user/<int:tg_id>', methods=['DELETE'])
@limiter.limit("500 per day")
@limiter.limit("2/seconds")
@auth.auth_required()
def delete_user(tg_id):
    data = [(tg_id)]
    UserRepository().deleteUser(data)
    return {'response': 'User successfully deleted'}