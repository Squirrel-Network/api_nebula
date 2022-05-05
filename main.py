#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import os
import time
from config import Config
from core.database.repository.superban import SuperbanRepository
from core.database.repository.users import UserRepository
from flask import Flask, request,render_template, send_from_directory
from flasgger import Swagger
from core.utilities.limiter import limiter
from core.utilities.auth_manager import auth
from core.utilities.functions import get_formatted_time
from core.api.test import api_test
from core.api.blacklist import api_blacklist
from core.api.users import api_users
from core.api.community import api_community
from core.api.groups import api_groups
from core.api.bot_service import api_bot_service
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
#Enable CORS Policy
CORS(app)

limiter.init_app(app)
auth.init_app(app)

Swagger(app,
    template_file='./openapi/main.yaml',
    merge=True,
    config={
        'title': 'Nebula API specs',
        'openapi': '3.0.0',
        'specs': [{
            'endpoint': 'openapi/specs',
            'route': '/openapi/specs.json'
        }],
    })

#############
### Home ###
############
@app.route('/')
def index():
    data = SuperbanRepository().getLastSuperBanned()
    for row in data:
        row['upper'] = row['user_first_name'][:1].upper()
        row['user_time'] = get_formatted_time(str(row['user_date']))
    countsb = SuperbanRepository().getCountSuperBanned()
    countsbNm = '{:20,}'.format(countsb['counter'])
    time_in_utc = datetime.utcnow()
    now_time = time_in_utc.strftime("%b %d %Y %H:%M %Z")
    return render_template("home.html", data = data, countsb = countsbNm, now_time = now_time)

###################
### User Search ###
###################
@app.route('/users', methods=['POST','GET'])
def users_search():
    if request.method == 'POST':
        username = request.form.get('username')
        if username is not None:
            data = UserRepository().getByUsername(username)
        return render_template("users.html", data = data)
    else:
        return render_template("users.html")

###################
### Fake Route  ###
###################
@app.route('/wp-admin', methods=['POST','GET'])
@app.route('/wp-login', methods=['POST','GET'])
@app.route('/admin', methods=['POST','GET'])
def fake_route():
    return render_template("fakeroute.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

####################
### API EndPoint ###
####################
app.register_blueprint(api_test, url_prefix='/v1')
app.register_blueprint(api_blacklist, url_prefix='/v1')
app.register_blueprint(api_users, url_prefix='/v1')
app.register_blueprint(api_community, url_prefix='/v1')
app.register_blueprint(api_groups, url_prefix='/v1')
app.register_blueprint(api_bot_service, url_prefix='/v1')

# setup defaults
defaults_values = {
    'PAGE_SIZE_DEFAULT': 50,
    'PAGE_SIZE_MAX': 1000
}

for k in defaults_values:
    if not app.config.get(k, None):
        app.config[k] = defaults_values[k]

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host='localhost')