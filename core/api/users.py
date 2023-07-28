#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from fastapi import APIRouter, Depends

from core.database.models import Users
from core.utilities.enums import OrderDir
from core.utilities.functions import format_iso_date, get_pagination_data
from core.utilities.rate_limiter import RateLimiter
from core.utilities.token_jwt import validate_token

api_users = APIRouter(prefix="/v1/users", tags=["users"])


@api_users.get(
    "/",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_token),
    ],
)
async def users(
    tg_username: str | None = None,
    start: int = 0,
    limit: int | None = None,
    order_by: str | None = None,
    order_dir: OrderDir = OrderDir.ASC,
):
    data = await get_pagination_data(
        Users,
        {"tg_username": tg_username} if tg_username else {},
        start,
        limit,
        order_by,
        order_dir,
    )

    return data


# @api_users.route("/users/<int:tg_id>", methods=["GET"])
# @rate_limit(2000, datetime.timedelta(days=1))
# @rate_limit(10, datetime.timedelta(seconds=1))
# @swag_from("../../openapi/users_get.yaml")
# def user_by_id(tg_id):
#     with UserRepository() as db:
#         row = db.get_by_id(int(tg_id))
#         if row:
#             return {
#                 "id": row["id"],
#                 "tg_id": row["tg_id"],
#                 "tg_username": row["tg_username"],
#                 "created_at": format_iso_date(row["created_at"]),
#                 "updated_at": format_iso_date(row["updated_at"]),
#             }
#         else:
#             return {
#                 "error": "You have entered an id that does not exist or you have entered incorrect data"
#             }, 404


# @api_users.route("/users/<int:tg_id>", methods=["DELETE"])
# @rate_limit(500, datetime.timedelta(days=1))
# @rate_limit(2, datetime.timedelta(seconds=1))
# @auth_required
# @swag_from("../../openapi/users_delete.yaml")
# def delete_user(tg_id):
#     with UserRepository() as db:
#         row = db.get_by_id(int(tg_id))
#         if row:
#             with UserRepository() as db:
#                 db.delete_user(int(tg_id))
#             return {"status": "I deleted user {} from the database".format(tg_id)}
#         else:
#             return {"error": "No user found"}, 404
