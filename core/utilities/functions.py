#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import time
from flask import current_app, request, Response, jsonify
from werkzeug.exceptions import abort
from datetime import datetime


def get_limit():
    limit = request.args.get("limit", current_app.config["PAGE_SIZE_DEFAULT"], type=int)
    if limit > current_app.config["PAGE_SIZE_MAX"]:
        limit = current_app.config["PAGE_SIZE_MAX"]
        print(limit)

    return limit


def get_pagination_headers():
    params = {
        "@start": request.args.get("start", 0, type=int),
        "@limit": get_limit(),
        "@order_dir": request.args.get("order_dir", "asc", type=str),
        "@order_field": request.args.get("order_by", None, type=str),
    }
    return params


def get_paginated_response(rows, total, pagination_info):
    start = pagination_info["@start"]
    limit = pagination_info["@limit"]
    next_page_start = start + limit
    next_link = ""
    if next_page_start < total:
        next_link = "start={0}&limit={1}".format(next_page_start, limit)

    prev_link = ""
    if start > 0:
        prev_link_start = start - limit
        if prev_link_start < 0:
            prev_link_start = 0
        prev_link = "start={0}&limit={1}".format(prev_link_start, limit)

    response = {
        "results": rows,
        "metadata": {
            "start": pagination_info["@start"],
            "limit": pagination_info["@limit"],
            "total": total,
            "next": next_link,
            "previous": prev_link,
        },
    }
    return response


def get_paginated_list(results, url, start, limit, count):
    start = int(start)
    limit = int(limit)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj["start"] = start
    obj["limit"] = limit
    obj["count"] = count
    # make URLs
    # make previous url
    if start == 1:
        obj["previous"] = ""
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj["next"] = ""
    else:
        start_copy = start + limit
        obj["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)
    # finally extract result according to bounds
    obj["results"] = results[(start - 1) : (start - 1 + limit)]
    return obj


def format_iso_date(d):
    """
    If the parameter is datetime format as iso, otherwise returns the same value
    """
    if type(d) is datetime:
        return d.isoformat()
    return d


def validation_error_response_handler(err, data, schema):
    # return { 'error': str(err)}, 400
    current_app.logger.warn("sdads")
    abort(
        Response(
            jsonify({"error": str(err), "data": data, "schema": schema}), status=400
        )
    )
    # abort({ 'error': str(err)}, 400)


def get_formatted_time(t: str) -> str:
    p_time = datetime.fromisoformat(t)
    c_time = datetime.fromtimestamp(time.time())
    if p_time.year == c_time.year:
        if p_time.month == c_time.month:
            if p_time.day == c_time.day:
                return f'{p_time.strftime("%H")}:{p_time.strftime("%M")}'
            elif p_time.isocalendar()[1] == c_time.isocalendar()[1]:
                return f'{p_time.strftime("%a")}'
        return f'{p_time.day} {p_time.strftime("%b")}'
    else:
        return f'{p_time.strftime("%m.%d.%Y")}'
