#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint, request, jsonify, abort
from flasgger import swag_from
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter
from core.utilities.functions import get_pagination_headers, format_iso_date, get_paginated_response
from core.database.repository.users import UserRepository

api_users = Blueprint('api_users', __name__)


@api_users.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
@swag_from('../../openapi/users_list.yaml')
def users():
    params = get_pagination_headers()
    params['tg_username'] = request.args.get('tg_username', None, type=str)

    rows = UserRepository().get_all(**params)
    count = UserRepository().count(**params)

    data = list(map(lambda row: {
        'id': row['id'],
        'tg_id': row['tg_id'],
        'tg_username': row['tg_username'],
        'created_at': format_iso_date(row['created_at']),
        'updated_at': format_iso_date(row['updated_at']),
    }, rows))

    return get_paginated_response(data, count, params)


@api_users.route('/users/<int:tg_id>', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@swag_from('../../openapi/users_get.yaml')
def user_by_id(tg_id):
    row = UserRepository().getById([tg_id])
    if row:
        return {
            'id': row['id'],
            'tg_id': row['tg_id'],
            'tg_username': row['tg_username'],
            'created_at': format_iso_date(row['created_at']),
            'updated_at': format_iso_date(row['updated_at']),
        }
    else:
        return {
            'error': 'You have entered an id that does not exist or you have entered incorrect data'
        }, 404


@api_users.route('/users/<int:tg_id>', methods=['DELETE'])
@limiter.limit("500 per day")
@limiter.limit("2/seconds")
@auth.auth_required()
@swag_from('../../openapi/users_delete.yaml')
def delete_user(tg_id):
    row = UserRepository().getById([tg_id])
    if row:
        data = [(tg_id)]
        UserRepository().deleteUser(data)
        return { 'status': 'ok' }
    else:
        return { 'error': 'No user found' }, 404
