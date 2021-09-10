#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint
from flasgger import swag_from
from core.utilities.limiter import limiter

api_test = Blueprint('api_test', __name__)

@api_test.route('/hi', methods=['GET'])
@limiter.limit("1000 per day")
@limiter.limit("3/seconds")
@swag_from('../../openapi/hi.yaml')
def hi():
    return { "status": "hi!" }