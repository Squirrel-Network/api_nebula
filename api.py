#!/usr/bin/env python
# encoding: utf-8
from config import Config
from database.repository.superban import SuperbanRepository
from flask import Flask, jsonify, request,render_template
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
    default_limits=["150 per minute", "1 per second"],
)

@app.route('/')
def index():
    data = SuperbanRepository().getLastSuperBanned()
    return render_template("home.html", data = data)

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
            return jsonify({'error': 'The user was not super banned or you entered an incorrect id'})
    else:
        return jsonify({'error': 'data not found'})


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)