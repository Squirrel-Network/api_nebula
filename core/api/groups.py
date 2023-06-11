#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flasgger import swag_from
from flask import Blueprint, jsonify

from core.database.repository.groups import GroupRepository
from core.utilities.limiter import limiter

api_groups = Blueprint("api_groups", __name__)


@api_groups.route("/groups", methods=["GET"])
@limiter.limit("5000 per day")
@limiter.limit("5/seconds")
def groups():
    return {"status": "Under Construction"}


@api_groups.route("/top_groups", methods=["GET"])
@limiter.limit("6000 per day")
@limiter.limit("10/seconds")
@swag_from("../../openapi/top_groups_list.yaml")
def groups_top_ten():
    with GroupRepository() as db:
        rows = db.top_ten_groups()

    return jsonify(rows)
