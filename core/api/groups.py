#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint, jsonify
from flasgger import swag_from
from core.utilities.limiter import limiter
from core.database.repository.groups import GroupRepository

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
    rows = GroupRepository().top_ten_groups()
    return jsonify(
        list(
            map(
                lambda row: {
                    "tg_group_id": row["tg_group_id"],
                    "tg_group_name": row["group_name"],
                    "total_message": row["counter"],
                },
                rows,
            )
        )
    )
