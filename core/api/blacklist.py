import datetime
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter
from core.database.repository.superban import SuperbanRepository
from core.utilities.functions import get_pagination_headers, format_iso_date, get_paginated_response

api_blacklist = Blueprint('api_blacklist', __name__)


@api_blacklist.route('/blacklist/<int:tg_id>', methods=['GET'])
@limiter.limit("1000 per day")
@limiter.limit("3/seconds")
@swag_from('../../openapi/blacklist.yaml')
def check_blacklist(tg_id):
    row = SuperbanRepository().getById([tg_id])
    if row:
        return {'tg_id': row['user_id'],
        'reason': row['motivation_text'],
        'date': row['user_date'].isoformat(), # TODO: manage dates in serializer
        'operator': row['id_operator']}
    else:
        return ({'error': 'The user was not superbanned or you entered an incorrect id'})

@api_blacklist.route('/blacklist', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
@swag_from('../../openapi/blacklist_list.yaml')
def blacklist():
    params = get_pagination_headers()
    params['user_id'] = request.args.get('user_id', None, type=int)
    params['motivation_text'] = request.args.get('motivation_text', None, type=str)
    params['id_operator'] = request.args.get('id_operator', None, type=int)

    rows = SuperbanRepository().get_all(**params)
    count = SuperbanRepository().count(**params)

    data = list(map(lambda row: {
            'id': row['id'],
            'user_id': row['user_id'],
            'motivation_text': row['motivation_text'],
            'user_date': format_iso_date(row['user_date']),
            'id_operator': row['id_operator'],
        }, rows))

    return get_paginated_response(data, count, params)


#TODO Auth Problem
@api_blacklist.route('/add_blacklist', methods=['POST'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def add_blacklist():
    user_id = request.args.get('tgid',type=int)
    motivation = request.args.get('motivation',type=str)
    date = datetime.datetime.utcnow().isoformat()
    operator_id = request.args.get('operator',type=int)
    data = [(user_id, motivation, date, operator_id)]
    row = SuperbanRepository().getById([user_id])
    if user_id is not None and user_id != "" and motivation is not None and motivation != "" and operator_id is not None and operator_id != "":
        if row:
            return {'error': 'The user has already been blacklisted'}
        else:
            SuperbanRepository().add(data)
            return {'response': 'User successfully blacklisted'}
    else:
        return {'error': 'Missing Parameters'}