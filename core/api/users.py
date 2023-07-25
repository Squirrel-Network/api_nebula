#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from flasgger import swag_from
from flask import Blueprint, request
from quart_rate_limiter import rate_limit

from core.database.repository.users import UserRepository
from core.decorators import auth_required
from core.utilities.functions import (
    format_iso_date,
    get_paginated_response,
    get_pagination_headers,
)

api_users = Blueprint("api_users", __name__)


@api_users.route("/users", methods=["GET"])
@rate_limit(5000, datetime.timedelta(days=1))
@rate_limit(10, datetime.timedelta(seconds=1))
@auth_required
@swag_from("../../openapi/users_list.yaml")
def users():
    params = get_pagination_headers()
    params["tg_username"] = request.args.get("tg_username", None, type=str)

    rows = UserRepository().get_all(**params)
    count = UserRepository().count(**params)

    data = list(
        map(
            lambda row: {
                "id": row["id"],
                "tg_id": row["tg_id"],
                "tg_username": row["tg_username"],
                "created_at": format_iso_date(row["created_at"]),
                "updated_at": format_iso_date(row["updated_at"]),
            },
            rows,
        )
    )

    return get_paginated_response(data, count, params)


@api_users.route("/users/<int:tg_id>", methods=["GET"])
@rate_limit(2000, datetime.timedelta(days=1))
@rate_limit(10, datetime.timedelta(seconds=1))
@swag_from("../../openapi/users_get.yaml")
def user_by_id(tg_id):
    with UserRepository() as db:
        row = db.get_by_id(int(tg_id))
        if row:
            return {
                "id": row["id"],
                "tg_id": row["tg_id"],
                "tg_username": row["tg_username"],
                "created_at": format_iso_date(row["created_at"]),
                "updated_at": format_iso_date(row["updated_at"]),
            }
        else:
            return {
                "error": "You have entered an id that does not exist or you have entered incorrect data"
            }, 404


@api_users.route("/users/<int:tg_id>", methods=["DELETE"])
@rate_limit(500, datetime.timedelta(days=1))
@rate_limit(2, datetime.timedelta(seconds=1))
@auth_required
@swag_from("../../openapi/users_delete.yaml")
def delete_user(tg_id):
    with UserRepository() as db:
        row = db.get_by_id(int(tg_id))
        if row:
            with UserRepository() as db:
                db.delete_user(int(tg_id))
            return {"status": "I deleted user {} from the database".format(tg_id)}
        else:
            return {"error": "No user found"}, 404
