#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from fastapi import APIRouter, Depends, HTTPException

from core.database.models import Users
from core.responses.base import GenericError, GenericResponse, NotAuthorizedResponse
from core.responses.users import (
    GetUserByIdResponse,
    GetUsersResponse,
    UserNotExistErrorModel,
)
from core.utilities.enums import OrderDir
from core.utilities.functions import get_pagination_data
from core.utilities.rate_limiter import RateLimiter
from core.utilities.token_jwt import validate_token

api_users = APIRouter(prefix="/users", tags=["users"])


@api_users.get(
    "/",
    summary="List of all users",
    description="List of all users",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_token),
    ],
    responses={
        200: {"model": GetUsersResponse, "description": "User list"},
        400: {"model": GenericError, "description": "Bad Request"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
    },
)
async def users(
    tg_username: str | None = None,
    page: int = 1,
    limit: int | None = None,
    order_by: str | None = None,
    order_dir: OrderDir = OrderDir.ASC,
):
    if page < 1:
        raise HTTPException(400, "Page must be greater than or equal to 1.")

    if limit is not None and limit < 0:
        raise HTTPException(400, "Limit must be greater than or equal to 0.")

    data, pages = await get_pagination_data(
        Users,
        {"tg_username": tg_username},
        page,
        limit,
        order_by,
        order_dir,
    )

    return GetUsersResponse(results=data, total_page=pages)


@api_users.get(
    "/{tg_id}",
    summary="Get user info",
    description="Get user info",
    dependencies=[
        Depends(RateLimiter(2000, days=1)),
        Depends(RateLimiter(10, 1)),
    ],
    responses={
        200: {"model": GetUserByIdResponse, "description": "User info"},
        404: {"model": UserNotExistErrorModel, "description": "User not exist"},
    },
)
async def user_by_id(tg_id: int):
    data = await Users.get_or_none(tg_id=tg_id)

    if not data:
        raise HTTPException(
            404,
            "You have entered an id that does not exist or you have entered incorrect data",
        )

    return GetUserByIdResponse(**await data.to_dict())


@api_users.delete(
    "/{tg_id}",
    summary="Delete a user",
    description="Delete a user",
    dependencies=[
        Depends(RateLimiter(500, days=1)),
        Depends(RateLimiter(2, 1)),
        Depends(validate_token),
    ],
    responses={
        200: {"model": GenericResponse, "description": "Operation successful"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
        404: {"model": UserNotExistErrorModel, "description": "User not exist"},
    },
)
async def delete_user(tg_id: int):
    data = await Users.get_or_none(tg_id=tg_id)

    if not data:
        raise HTTPException(
            404,
            "You have entered an id that does not exist or you have entered incorrect data",
        )

    await data.delete()

    return GenericResponse(status=f"I deleted user {tg_id} from the database")
