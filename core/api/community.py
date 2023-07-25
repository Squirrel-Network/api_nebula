#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify
from quart_rate_limiter import rate_limit

from core.database.repository.community import CommunityRepository

api_community = Blueprint("api_community", __name__)


@api_community.route("/community", methods=["GET"])
@rate_limit(5000, datetime.timedelta(days=1))
@rate_limit(5, datetime.timedelta(seconds=1))
def community():
    return {"status": "Under Construction"}


@api_community.route("/top_community", methods=["GET"])
@rate_limit(5000, datetime.timedelta(days=1))
@rate_limit(10, datetime.timedelta(seconds=1))
@swag_from("../../openapi/top_community_list.yaml")
def top_ten_community():
    with CommunityRepository() as db:
        rows = db.top_ten_communities()

    return jsonify(rows)
