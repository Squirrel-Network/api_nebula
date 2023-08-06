#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from fastapi import APIRouter, Depends
from tortoise.functions import Count

from config import Session
from core.database.models import Community, Groups, NebulaUpdates
from core.responses.statistics import CommunityTopTenResponse, GroupsTopTenResponse
from core.utilities.rate_limiter import RateLimiter

api_statistics = APIRouter(prefix="/statistics", tags=["statistics"])


async def get_top_10_frequent_groups():
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
    result = []

    subquery = (
        await NebulaUpdates.filter(date__gte=last_30_days)
        .exclude(tg_group_id=Session.config.STAFF_GROUP_ID)
        .annotate(counter=Count("tg_group_id"))
        .group_by("tg_group_id")
        .order_by("-counter")
        .limit(10)
        .values("tg_group_id", "counter")
    )

    for x in subquery:
        group = await Groups.get(id_group=x["tg_group_id"])

        result.append(
            {
                "tg_group_id": x["tg_group_id"],
                "tg_group_name": group.group_name,
                "total_message": x["counter"],
            }
        )

    return result


async def get_top_10_frequent_community():
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
    result = []

    subquery = (
        await NebulaUpdates.filter(date__gte=last_30_days)
        .exclude(tg_group_id=Session.config.STAFF_GROUP_ID)
        .annotate(counter=Count("tg_group_id"))
        .group_by("tg_group_id")
        .order_by("-counter")
        .values("tg_group_id", "counter")
    )

    group_ids = {x["tg_group_id"]: x["counter"] for x in subquery}

    communities = (
        await Community.filter(tg_group_id__in=group_ids.keys())
        .limit(10)
        .values("tg_group_id", "tg_group_name", "tg_group_link", "language", "type")
    )

    for x in communities:
        group = await Groups.get(id_group=x["tg_group_id"])

        result.append(
            {
                "chat_type": x["type"],
                "group_photo": group.group_photo,
                "language": group.languages,
                "tg_group_id": x["tg_group_id"],
                "tg_group_link": x["tg_group_link"],
                "tg_group_name": x["tg_group_name"],
                "total_message": group_ids[x["tg_group_id"]],
                "total_users": group.total_users,
            }
        )

    return result


@api_statistics.get(
    "/top_groups",
    summary="Statistics about the top groups",
    description="Statistics about the top groups",
    dependencies=[
        Depends(RateLimiter(6000, days=1)),
        Depends(RateLimiter(10, 1)),
    ],
    responses={
        200: {"model": GroupsTopTenResponse, "description": "Top groups"},
    },
)
async def groups_top_ten():
    return GroupsTopTenResponse(results=await get_top_10_frequent_groups())


@api_statistics.get(
    "/top_community",
    summary="Statistics about the top communitis",
    description="Statistics about the top communitis",
    dependencies=[
        Depends(RateLimiter(6000, days=1)),
        Depends(RateLimiter(10, 1)),
    ],
    responses={
        200: {"model": CommunityTopTenResponse, "description": "Top groups"},
    },
)
async def community_top_ten():
    return CommunityTopTenResponse(results=await get_top_10_frequent_community())
