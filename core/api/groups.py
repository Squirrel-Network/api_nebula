#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify
from quart_rate_limiter import rate_limit

from core.database.repository.groups import GroupRepository

api_groups = Blueprint("api_groups", __name__)


@api_groups.route("/groups", methods=["GET"])
@rate_limit(5000, datetime.timedelta(days=1))
@rate_limit(5, datetime.timedelta(seconds=1))
def groups():
    return {"status": "Under Construction"}


@api_groups.route("/top_groups", methods=["GET"])
@rate_limit(6000, datetime.timedelta(days=1))
@rate_limit(10, datetime.timedelta(seconds=1))
@swag_from("../../openapi/top_groups_list.yaml")
def groups_top_ten():
    with GroupRepository() as db:
        rows = db.top_ten_groups()

    return jsonify(rows)
