import datetime
from flask import Blueprint, request, jsonify
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter
from core.database.repository.superban import SuperbanRepository
from core.utilities.functions import get_limit

api_blacklist = Blueprint('api_blacklist', __name__)


@api_blacklist.route('/check_blacklist/<int:tg_id>', methods=['GET'])
@limiter.limit("1000 per day")
@limiter.limit("3/seconds")
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
def blacklist():
    limit = get_limit(api_blacklist)
    countsb = SuperbanRepository().getCountSuperBanned()
    total = countsb['counter']
    print(total)
    rows = SuperbanRepository().getAll([limit])

    return jsonify(list(map(lambda row: {
        'id': row['id'],
        'tg_id': row['user_id'],
        'motivation': row['motivation_text'],
        'date': row['user_date'].isoformat(),
        'operator': row['id_operator']
    }, rows)))

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
            return {'response': 'The user has already been blacklisted'}
        else:
            SuperbanRepository().add(data)
            return {'response': 'User successfully blacklisted'}
    else:
        return {'response': 'Missing Parameters'}