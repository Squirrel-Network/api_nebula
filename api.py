#!/usr/bin/env python
# encoding: utf-8
import datetime
from flask.json import jsonify
from config import Config
from database.repository.superban import SuperbanRepository
from database.repository.users import UserRepository
from flask import Flask, request,render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from auth_manager import setup_auth

app = Flask(__name__)
app.config.from_object(Config)
#Enable CORS Policy
CORS(app)

auth = setup_auth(app)

#Limit Request
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["150 per minute", "2 per second"],
)


# setup defaults
defaults_values = {
    'PAGE_SIZE_DEFAULT': 50,
    'PAGE_SIZE_MAX': 200
}

for k in defaults_values:
    app.logger.warn('check %s', k)
    if not app.config.get(k, None):
        app.logger.warn('adding %s', k)
        app.config[k] = defaults_values[k]


def get_limit():
    limit = request.args.get('limit', app.config['PAGE_SIZE_DEFAULT'], type=int)
    if limit > app.config['PAGE_SIZE_MAX']:
        limit = app.config['PAGE_SIZE_MAX']

    return limit

#############
### Home ###
############
@app.route('/')
def index():
    data = SuperbanRepository().getLastSuperBanned()
    countsb = SuperbanRepository().getCountSuperBanned()
    return render_template("home.html", data = data, countsb = countsb['counter'])


@app.route('/hi')
@auth.auth_required()
def hi():
    return { "status": "hi!" }

##########################
### Blacklist Endpoint ###
##########################
@app.route('/blacklist', methods=['GET'])
@limiter.limit("1000 per day")
@limiter.limit("3/seconds")
def blacklist():
    user_id = request.args.get('tgid',type=int)
    if user_id is not None and user_id != "":
        user_id = int(user_id)
        row = SuperbanRepository().getById([user_id])
        if row:
            return {'tg_id': row['user_id'],
            'reason': row['motivation_text'],
            'date': row['user_date'].isoformat(), # TODO: manage dates in serializer
            'operator': row['id_operator']}
        else:
            return ({'error': 'The user was not superbanned or you entered an incorrect id'})
    else:
        return ({'error': 'missing or invalid tgid'}, 400)

@app.route('/getblacklist', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def get_blacklist():
    limit = get_limit()

    rows = SuperbanRepository().getAll([limit])

    return jsonify(list(map(lambda row: {
        'id': row['id'],
        'tg_id': row['user_id'],
        'motivation': row['motivation_text'],
        'date': row['user_date'].isoformat(),
        'operator': row['id_operator']
    }, rows)))


@app.route('/add_blacklist', methods=['POST'])
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

###########################
### User/Users Endpoint ###
###########################
@app.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def users():
    limit = get_limit()

    if limit > 100:
        limit = 100

    rows = UserRepository().getAll([limit])

    return jsonify(list(map(lambda row: {
        'id': row['id'],
        'tg_id': row['tg_id'],
        'username': row['tg_username'],
        'warn': row['warn_count'],
    }, rows)))

@app.route('/user', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def user():
    user_id = request.args.get('tgid',type=int)
    user_id = int(user_id)
    row = UserRepository().getById([user_id])
    if row:
        return {'id': row['id'],
        'tg_id': row['tg_id'],
        'username': row['tg_username'],
        'warn': row['warn_count']}
    else:
        return {'error': 'You have entered an id that does not exist or you have entered incorrect data'}

@app.route('/delete_user', methods=['DELETE'])
@limiter.limit("500 per day")
@limiter.limit("2/seconds")
@auth.auth_required()
def delete_user():
    user_id = request.args.get('tgid',type=int)
    data = [(user_id)]
    UserRepository().deleteUser(data)
    return {'response': 'User successfully deleted'}


if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host='localhost')