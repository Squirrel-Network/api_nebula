#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint, request
from core.utilities.limiter import limiter

api_community = Blueprint('api_community', __name__)

@api_community.route('/community', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("5/seconds")
def community():
    return { "status": "Under Construction" }

@api_community.route('/top_community', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
def top_ten_community():
    return { "status": "Under Construction" }