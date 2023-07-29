#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from fastapi import APIRouter, Depends
from tortoise.functions import Count

from core.database.models import NebulaUpdates
from core.responses.base import GenericResponse
from core.utilities.rate_limiter import RateLimiter

api_groups = APIRouter(prefix="/v1/top_groups", tags=["community"])


async def get_top_10_frequent_groups():
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)

    subquery = (
        await NebulaUpdates.filter(date__gte=last_30_days)
        .annotate(count=Count("tg_group_id"))
        .group_by("tg_group_id")
        .order_by("-count")
        .values("tg_group_id", "count")
    )

    return subquery


@api_groups.get(
    "/",
    summary="Statistics about the top groups",
    description="Statistics about the top groups",
    dependencies=[
        Depends(RateLimiter(6000, days=1)),
        Depends(RateLimiter(10, 1)),
    ],
    responses={
        200: {"model": GenericResponse, "description": "Top groups"},
    },
)
async def groups_top_ten():
    return await get_top_10_frequent_groups()
