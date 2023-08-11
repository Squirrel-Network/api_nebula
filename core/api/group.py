#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from fastapi import APIRouter, Depends, HTTPException

from core.database.models import Groups, GroupsFilters, NebulaUpdates
from core.responses.base import GenericError, GenericResponse, NotAuthorizedResponse
from core.responses.group import (
    ChangeGroupFiltersPayload,
    GetGroupFilters,
    GetGroupInfo,
)
from core.utilities.rate_limiter import RateLimiter
from core.utilities.telegram_auth import validate_telegram

api_group = APIRouter(prefix="/group", tags=["group"])


async def get_group_messages(chat_id: int):
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)

    subquery = await NebulaUpdates.filter(
        date__gte=last_30_days, tg_group_id=chat_id
    ).count()

    return subquery


@api_group.get(
    "/{chat_id}",
    summary="Get info of group",
    description="Get info of group",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_telegram),
    ],
    responses={
        200: {"model": GetGroupInfo, "description": "Group info"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
        404: {"model": GenericError, "description": "Chat_id not found"},
    },
)
async def get_group_info(chat_id: int):
    data = await Groups.get_or_none(id_group=chat_id)

    if not data:
        raise HTTPException(404, "chat_id does not exist")

    return GetGroupInfo(
        **await data.get_info(), total_messages=await get_group_messages(chat_id)
    )


@api_group.get(
    "/{chat_id}/filters",
    summary="List of group filters",
    description="List of group filters",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_telegram),
    ],
    responses={
        200: {"model": GetGroupFilters, "description": "Filters list"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
        404: {"model": GenericError, "description": "Chat_id not found"},
    },
)
async def get_filters_settings(chat_id: int):
    data = await GroupsFilters.get_or_none(chat_id=chat_id)

    if not data:
        raise HTTPException(404, "chat_id does not exist")

    return GetGroupFilters(**await data.get_filters())


@api_group.post(
    "/{chat_id}/filters",
    summary="Change group filters",
    description="Change group filters",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_telegram),
    ],
    responses={
        200: {"model": GenericResponse, "description": "User list"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
        404: {"model": GenericError, "description": "Chat_id not found"},
    },
)
async def change_filters_settings(chat_id: int, data: ChangeGroupFiltersPayload):
    group = await GroupsFilters.get_or_none(chat_id=chat_id)

    if not group:
        raise HTTPException(404, "chat_id does not exist")

    await group.update_from_dict(data.model_dump()).save()

    return GenericResponse(status="ok")
