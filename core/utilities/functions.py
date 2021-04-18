from flask import request

def get_limit(app):
    limit = request.args.get('limit', app.config['PAGE_SIZE_DEFAULT'], type=int)
    if limit > app.config['PAGE_SIZE_MAX']:
        limit = app.config['PAGE_SIZE_MAX']

    return limit