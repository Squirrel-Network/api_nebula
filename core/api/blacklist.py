#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import IntegrityError

from core.database.models import SuperbanTable
from core.responses.base import GenericError, GenericResponse, NotAuthorizedResponse
from core.responses.blacklist import (
    AddBlacklistUserPayload,
    GetBlacklistUserResponse,
    GetListBlacklistResponse,
    UserNotFound,
)
from core.utilities.enums import OrderDir
from core.utilities.functions import get_pagination_data
from core.utilities.rate_limiter import RateLimiter
from core.utilities.token_jwt import validate_token

api_blacklist = APIRouter(prefix="/blacklist", tags=["blacklist"])


@api_blacklist.get(
    "/",
    summary="List of blacklisted users",
    description="List of blacklisted users",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_token),
    ],
    responses={
        200: {"model": GetListBlacklistResponse, "description": "User list"},
        400: {"model": GenericError, "description": "Bad Request"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
    },
)
async def list_blacklist(
    motivation_text: str | None = None,
    id_operator: int | None = None,
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
        SuperbanTable,
        {"motivation_text": motivation_text, "id_operator": id_operator},
        page,
        limit,
        order_by,
        order_dir,
    )

    return GetListBlacklistResponse(results=data, total_page=pages)


@api_blacklist.get(
    "/{tg_id}",
    summary="Check if a user is blacklisted",
    description="Check if a user is blacklisted",
    dependencies=[
        Depends(RateLimiter(1500, days=1)),
        Depends(RateLimiter(3, 1)),
    ],
    responses={
        200: {"model": GetBlacklistUserResponse, "description": "Blacklisted user"},
        404: {"model": UserNotFound, "description": "The user is not blacklisted"},
    },
)
async def get_blacklist(tg_id: int):
    user = await SuperbanTable.get_or_none(user_id=tg_id)

    if not user:
        raise HTTPException(
            404, "The user was not superbanned or you entered an incorrect id"
        )

    return GetBlacklistUserResponse(**await user.to_dict())


@api_blacklist.post(
    "/",
    summary="Add blacklisted user",
    description="Add blacklisted user",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_token),
    ],
    responses={
        200: {"model": GenericResponse, "description": "Operation successful"},
        400: {"model": GenericError, "description": "Bad Request"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
    },
)
async def add_blacklist(user_payload: AddBlacklistUserPayload):
    try:
        await SuperbanTable.create(
            user_id=user_payload.user_id,
            user_first_name=user_payload.user_first_name,
            motivation_text=user_payload.motivation_text,
            id_operator=user_payload.id_operator,
            username_operator=user_payload.username_operator,
            first_name_operator=user_payload.first_name_operator,
        )
    except IntegrityError:
        raise HTTPException(400, "The user has already been blacklisted")

    return GenericResponse(status="ok")
