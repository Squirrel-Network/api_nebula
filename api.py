#!/usr/bin/env python
# encoding: utf-8
from config import Config
from database.repository.superban import SuperbanRepository
from database.repository.users import UserRepository
from flask import Flask, Response, jsonify, request,render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

app = Flask(__name__)
#Enable CORS Policy
CORS(app)

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
            return jsonify({'tg_id': row['user_id'],
            'reason': row['motivation_text'],
            'date': row['user_date'],
            'operator': row['id_operator']})
        else:
            return jsonify({'error': 'The user was not superbanned or you entered an incorrect id'})
    else:
        return jsonify({'error': 'data not found'})


@app.route('/add_blacklist', methods=['POST'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
def add_blacklist():
    user_id = request.args.get('tgid',type=int)
    motivation = request.args.get('motivation',type=str)
    date = request.args.get('date',type=str)
    operator_id = request.args.get('operator',type=int)
    token = request.args.get('token')
    if token == Config.TOKEN and token is not None and token != "":
        print(user_id)
        print(motivation)
        print(date)
        print(operator_id)
        print(token)
    else:
        return jsonify({'error': "You don't have permission to access this api"})
    return jsonify({'user': user_id,'motivation': motivation, 'date': date, 'operator': operator_id, 'token': token})

###########################
### User/Users Endpoint ###
###########################
@app.route('/users', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
def users():
    limit = request.args.get('limit', type=int)
    token = request.args.get('token')
    rows = UserRepository().getAll([limit])

    if limit is not None and limit != "" and token == Config.TOKEN and token is not None and token != "":
        return jsonify(list(map(lambda row: {'id': row['id'],'tg_id': row['tg_id'],'username': row['tg_username'],'warn': row['warn_count']}, rows)))
    else:
        return jsonify({'error': "You don't have permission to access this api"})

@app.route('/user', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
def user():
    user_id = request.args.get('tgid',type=int)
    token = request.args.get('token')
    if user_id is not None and user_id != "" and token == Config.TOKEN and token is not None and token != "":
        user_id = int(user_id)
        row = UserRepository().getById([user_id])
        if row:
            return jsonify({'id': row['id'],
            'tg_id': row['tg_id'],
            'username': row['tg_username'],
            'warn': row['warn_count']})
        else:
            return jsonify({'error': 'You have entered an id that does not exist or you have entered incorrect data'})
    else:
        return jsonify({'error': "You don't have permission to access this api"})

@app.route('/delete_user', methods=['DELETE'])
@limiter.limit("500 per day")
@limiter.limit("2/seconds")
def delete_user():
    user_id = request.args.get('tgid',type=int)
    token = request.args.get('token')
    if user_id is not None and user_id != "" and token == Config.TOKEN and token is not None and token != "":
        data = [(user_id)]
        UserRepository().deleteUser(data)
        return jsonify({'response': 'User successfully deleted'})
    else:
        return jsonify({'error': "You don't have permission to access this api"})



if __name__ == "__main__":
    app.run(debug=Config.DEBUG)