#!/usr/bin/env python
# encoding: utf-8
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


@app.route('/add_blacklist', methods=['POST'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def add_blacklist():
    user_id = request.args.get('tgid',type=int)
    motivation = request.args.get('motivation',type=str)
    date = request.args.get('date',type=str)
    operator_id = request.args.get('operator',type=int)
    print(user_id)
    print(motivation)
    print(date)
    print(operator_id)
    return {'user': user_id,'motivation': motivation, 'date': date, 'operator': operator_id }

###########################
### User/Users Endpoint ###
###########################
@app.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth.auth_required()
def users():
    limit = request.args.get('limit', 50, type=int)
    
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
    #app.run(debug=True , host='0.0.0.0')
    app.run(debug=Config.DEBUG, host=Config.FLASK_HOST)
