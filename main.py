#!/usr/bin/env python
# encoding: utf-8
import datetime
from flask.json import jsonify
from config import Config
from core.database.repository.superban import SuperbanRepository
from flask import Flask, request,render_template
from flasgger import Swagger
from core.utilities.limiter import limiter
from core.utilities.auth_manager import auth
from core.api.test import api_test
from core.api.blacklist import api_blacklist
from core.api.users import api_users
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
    countsb = SuperbanRepository().getCountSuperBanned()
    return render_template("home.html", data = data, countsb = countsb['counter'])

####################
### API EndPoint ###
####################
app.register_blueprint(api_test, url_prefix='/v1')
app.register_blueprint(api_blacklist, url_prefix='/v1')
app.register_blueprint(api_users, url_prefix='/v1')

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