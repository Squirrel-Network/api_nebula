#!/usr/bin/env python
# encoding: utf-8
import json
from database.repository.superban import SuperbanRepository
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'error': 'Not Found'})

@app.route('/blacklist', methods=['GET'])
def blacklist():
    user_id = request.args.get('tgid')
    if user_id is not None and user_id != "":
        user_id = int(user_id)
        row = SuperbanRepository().getById([user_id])
        if row:
            return jsonify({'tg_id': row['user_id'],
            'motivation': row['motivation_text'],
            'user_date': row['user_date'],
            'id_operator': row['id_operator']})
        else:
            return jsonify({'error': 'The user was not superanned or you entered an incorrect id'})
    else:
        return jsonify({'error': 'data not found'})

app.run(host='0.0.0.0',port=5000,debug=True)