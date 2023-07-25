#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from flasgger import swag_from
from flask import Blueprint
from quart_rate_limiter import rate_limit

api_test = Blueprint("api_test", __name__)


@api_test.route("/", methods=["GET"])
@rate_limit(1000, datetime.timedelta(days=1))
@rate_limit(3, datetime.timedelta(seconds=1))
@swag_from("../../openapi/hi.yaml")
def hi():
    return {"status": "hi!"}
