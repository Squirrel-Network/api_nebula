from flask import current_app, request

def get_limit(app):
    limit = request.args.get('limit', current_app.config['PAGE_SIZE_DEFAULT'], type=int)
    if limit > current_app.config['PAGE_SIZE_MAX']:
        limit = current_app.config['PAGE_SIZE_MAX']

    return limit