#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flasgger import swag_from
from flask import Blueprint, jsonify

from core.database.repository.community import CommunityRepository
from core.utilities.limiter import limiter

api_community = Blueprint("api_community", __name__)


@api_community.route("/community", methods=["GET"])
@limiter.limit("5000 per day")
@limiter.limit("5/seconds")
def community():
    return {"status": "Under Construction"}


@api_community.route("/top_community", methods=["GET"])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@swag_from("../../openapi/top_community_list.yaml")
def top_ten_community():
    with CommunityRepository() as db:
        rows = db.top_ten_communities()

    return jsonify(rows)
