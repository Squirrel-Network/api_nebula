#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import math
from datetime import datetime

from tortoise.models import Model

from config import Session
from core.utilities.enums import OrderDir


def get_limit(limit: int | None):
    if not limit:
        limit = Session.config.PAGE_SIZE_DEFAULT

    if limit > (size_max := Session.config.PAGE_SIZE_MAX):
        limit = size_max

    return limit


def get_formatted_time(t: str) -> str:
    p_time = datetime.fromisoformat(t)
    c_time = datetime.now()

    if p_time.year == c_time.year:
        if p_time.date() == c_time.date():
            return p_time.strftime("%H:%M")
        elif p_time.isocalendar()[1] == c_time.isocalendar()[1]:
            return p_time.strftime("%a")
        else:
            return p_time.strftime("%d %b")
    else:
        return p_time.strftime("%m.%d.%Y")


async def get_pagination_data(
    model: Model,
    params: dict,
    page: int,
    limit: int | None,
    order_by: str | None,
    order_dir: OrderDir,
):
    limit = get_limit(limit)
    params = {k: v for k, v in params.items() if v}
    query = model.all().filter(**params).offset((page - 1) * limit).limit(limit)

    if order_by and order_by in model._meta.fields_map.keys():
        query = query.order_by(
            order_by if order_dir == OrderDir.ASC else f"-{order_by}"
        )

    total_page = math.ceil(await model.all().count() / limit)

    if hasattr(model, "to_dict"):
        result = [await x.to_dict() async for x in query]
    else:
        result = await query.values()

    return result, total_page
