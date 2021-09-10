#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint, request
from core.utilities.limiter import limiter

api_groups = Blueprint('api_groups', __name__)

@api_groups.route('/groups', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("5/seconds")
def groups():
    return { "status": "Under Construction" }