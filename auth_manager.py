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
            return ({'error': 'missing token'}, 400)

        if not token in app.config['TOKENS']:
            return ({'error': 'not authorized'}, 403)

        expires = datetime.utcnow() + \
            timedelta(minutes=app.config['TOKEN_DURATION_MINUTES'])
        jwt_token = jwt.encode({
            "auth": "true",
            "exp": expires,
            "iss": "nebula_api",
        }, app.config['SECRET'], algorithm="HS256")

        return {"token": jwt_token}

    return Auth(app)


class Auth:
    def __init__(self, app):
        self.app = app

    def _discover_token(self):
        """
        Search for token in Authorization header as bearer token or in token query string parameter
        """
        auth_header = request.headers.get('authorization', None)
        if auth_header:
            header_segments = [s for s in auth_header.split(' ') if s]
            if len(header_segments) >= 2 \
                    and header_segments[0].lower() == 'bearer' \
                    and header_segments[1]:
                return header_segments[1]
        return request.args.get('token', None)

    def validate_token(self, token):
        data = None
        decode_config = {
            'algorithms': ['HS256'],
        }
        try:
            data = jwt.decode(
                token, self.app.config['SECRET'], **decode_config)
        except Exception as e:
            self.app.logger.warning("Invalid token: %s", e)

        return data

    def auth_required(self):
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):

                token = self._discover_token()

                token_data = self.validate_token(token) if token else None

                if not token_data:
                    return ({'error': 'not authorized'}, 401)

                return fn(*args, **kwargs)

            return decorator
        return wrapper
