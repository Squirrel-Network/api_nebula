#!/usr/bin/env python
# encoding: utf-8
import datetime
from flask.json import jsonify
from config import Config
from core.database.repository.superban import SuperbanRepository
from core.database.repository.users import UserRepository
from flask import Flask, request,render_template
from core.utilities.limiter import limiter
from core.utilities.auth_manager import auth
from core.api.test import api_test
from core.api.blacklist import api_blacklist
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
#Enable CORS Policy
CORS(app)

limiter.init_app(app)
auth.init_app(app)

app.register_blueprint(api_test, url_prefix='/api/v1')
app.register_blueprint(api_blacklist, url_prefix='/api/v1')

#app.register_blueprint(api)

# setup defaults
defaults_values = {
    'PAGE_SIZE_DEFAULT': 50,
    'PAGE_SIZE_MAX': 200
}

for k in defaults_values:
    print('check %s', k)
    if not app.config.get(k, None):
        print('adding %s', k)
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



##########################
### Blacklist Endpoint ###
##########################







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