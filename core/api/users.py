from flask import Blueprint, request, jsonify, abort
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter
from core.utilities.functions import get_limit, get_paginated_list
from core.database.repository.users import UserRepository

api_users = Blueprint('api_users', __name__)

@api_users.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def users():
    username = request.args.get('username',type=str)
    order_by = request.args.get('orderby',type=int)
    start= request.args.get('start', 1, type=int)
    limit= request.args.get('limit', 20, type=int)
    data_start = (start,limit)
    rows = UserRepository().getAll(data_start)
    countuser = UserRepository().getCountUsers()
    total = countuser['counter']
    data = list(map(lambda row: {
            'id': row['id'],
            'tg_id': row['tg_id'],
            'username': row['tg_username'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        }, rows))

    if username is not None and username != "":
        row = UserRepository().getByUsername(username)
        if row:
            return {'id': row['id'],
            'tg_id': row['tg_id'],
            'username': row['tg_username'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']}
        else:
            return {'error': 'You have entered an username that does not exist or you have entered incorrect data'}

    if order_by == 1:
        print("ASC")
        return {'response': 'ASC'}
    elif order_by == 2:
        print("DESC")
        return {'response': 'DESC'}
    elif order_by == 3:
        print("Order by Username")
        return {'response': 'Order by Username'}
    elif order_by == 4:
        print("Order by tgid")
        return {'response': 'Order by tgid'}
    else:
        return jsonify(get_paginated_list(
        data,
        '/page',
        start,
        limit,
        total
        ))

@api_users.route('/users/<int:tg_id>', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def user_by_id(tg_id):
    row = UserRepository().getById([tg_id])
    if row:
        return {'id': row['id'],
        'tg_id': row['tg_id'],
        'username': row['tg_username'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']}
    else:
        return {'error': 'You have entered an id that does not exist or you have entered incorrect data'}

@api_users.route('/users/delete_user/<int:tg_id>', methods=['DELETE'])
@limiter.limit("500 per day")
@limiter.limit("2/seconds")
@auth.auth_required()
def delete_user(tg_id):
    row = UserRepository().getById([tg_id])
    if row:
        data = [(tg_id)]
        UserRepository().deleteUser(data)
        return {'response': 'User successfully deleted'}
    else:
        return {'error': 'There is no user with this id to delete'}