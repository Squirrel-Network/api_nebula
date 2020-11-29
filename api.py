#!/usr/bin/env python
# encoding: utf-8
import json
from database.repository.superban import SuperbanRepository
from flask import Flask, jsonify, request,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/blacklist', methods=['GET'])
def blacklist():
    user_id = request.args.get('tgid',type=int)
    if user_id is not None and user_id != "":
        user_id = int(user_id)
        row = SuperbanRepository().getById([user_id])
        if row:
            return jsonify({'tg_id': row['user_id'],
            'motivation': row['motivation_text'],
            'user_date': row['user_date'],
            'id_operator': row['id_operator']})
        else:
            return jsonify({'error': 'The user was not super banned or you entered an incorrect id'})
    else:
        return jsonify({'error': 'data not found'})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)