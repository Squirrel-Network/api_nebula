from flask import Blueprint, request, jsonify, abort
from flasgger import swag_from
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter
from core.utilities.functions import get_limit, get_paginated_list
from core.database.repository.users import UserRepository

api_users = Blueprint('api_users', __name__)

@api_users.route('/paginationtest/page')
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def view():
    data = [{'telegram_id': i+1} for i in range(1000)]
    return jsonify(get_paginated_list(
        data,
        '/events/page',
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 20)
        ))

@api_users.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
@swag_from('../../openapi/users_list.yaml')
def users():
    start = 10
    limit = get_limit(api_users)
    countus = UserRepository().getCountUsers()
    total = countus['counter']
    username = request.args.get('username',type=str)
    order_by = request.args.get('orderby',type=int)

    #if limit > 100:
        #limit = 200
    print(start)
    print(limit)
    print(total)

    if username is not None and username != "":
        row = UserRepository().getByUsername(username)
        if row:
            return {'id': row['id'],
            'tg_id': row['tg_id'],
            'username': row['tg_username'],
            'warn': row['warn_count']}
        else:
            return {'error': 'You have entered an username that does not exist or you have entered incorrect data'}

    rows = UserRepository().getAll([limit])
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
def user_by_id(tg_id):
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
    row = UserRepository().getById([tg_id])
    if row:
        data = [(tg_id)]
        UserRepository().deleteUser(data)
        return {'response': 'User successfully deleted'}
    else:
        return {'response': 'There is no user with this id to delete'}