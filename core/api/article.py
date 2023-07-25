#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from flask import Blueprint, jsonify
from quart_rate_limiter import rate_limit

from core.database.repository.groups import GroupRepository
from core.utilities.functions import format_iso_date

api_article = Blueprint("api_article", __name__)


@api_article.route("/", methods=["GET"])
@rate_limit(3000, datetime.timedelta(days=1))
@rate_limit(5, datetime.timedelta(seconds=1))
def article():
    with GroupRepository() as db:
        articles = db.get_article()

    return jsonify(
        list(
            map(
                lambda row: {
                    **row,
                    "created_at": format_iso_date(row["created_at"]),
                    "updated_at": format_iso_date(row["updated_at"]),
                },
                articles,
            )
        )
    )
