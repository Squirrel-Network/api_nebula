from flask import Flask, request

def get_limit(app: Flask):
    limit = request.args.get('limit', app.config['PAGE_SIZE_DEFAULT'], type=int)
    if limit > app.config['PAGE_SIZE_MAX']:
        limit = app.config['PAGE_SIZE_MAX']

    return limit