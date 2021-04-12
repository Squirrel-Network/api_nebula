# encoding: utf-8
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request
import jwt

def setup_auth(app: Flask):

    config_token = app.config['TOKEN'] or ''
    app.config['TOKENS'] = [t.strip() for t in config_token.split(',') if t]
    
    @app.route('/authenticate', methods=['POST'])
    def authenticate():
        token = None
        if request.json: 
                token = request.json.get('token', None)
        elif request.form:
                token = request.form.get('token', None)

        if not token:
                return ({ 'error': 'missing token' }, 400)
        
        if not token in app.config['TOKENS']:
            return ({ 'error': 'not authorized' }, 403) 

        expires = datetime.utcnow() + timedelta(minutes=app.config['TOKEN_DURATION_MINUTES'])
        jwt_token = jwt.encode({
                "auth": "true",
                "exp": expires,
                "iss": "nebula_api",
        }, app.config['SECRET'], algorithm="HS256" ) 

        return { "token": jwt_token}

    return Auth(app)

class Auth:
  def __init__(self, app):
     self.app = app

  def auth_required(self):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # TODO: here

            #self.app.logger.debug('----')
            return fn(*args, **kwargs)

        return decorator
    return wrapper