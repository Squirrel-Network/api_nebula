#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from fastapi import APIRouter, Depends
from tortoise.functions import Count

from core.database.models import Community, Groups, NebulaUpdates
from core.responses.base import GenericResponse
from core.responses.statistics import GroupsTopTenResponse
from core.utilities.rate_limiter import RateLimiter

api_statistics = APIRouter(prefix="/v1/statistics", tags=["statistics"])


async def get_top_10_frequent_groups():
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
    result = []

    subquery = (
        await NebulaUpdates.filter(date__gte=last_30_days)
        .annotate(counter=Count("tg_group_id"))
        .group_by("tg_group_id")
        .order_by("-counter")
        .limit(10)
        .values("tg_group_id", "counter")
    )

    for x in subquery:
        group = await Groups.get(id_group=x["tg_group_id"])
        community = await Community.get(tg_group_id=x["tg_group_id"])

        result.append(
            {
                "counter": x["counter"],
                "group_name": group.group_name,
                "group_photo": group.group_photo,
                "language": group.languages,
                "tg_group_id": x["tg_group_id"],
                "tg_group_link": community.tg_group_link,
                "total_users": group.total_users,
                "type": community.type,
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
