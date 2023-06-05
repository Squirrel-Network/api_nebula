#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, jsonify

from core.database.repository.groups import GroupRepository
from core.utilities.functions import format_iso_date
from core.utilities.limiter import limiter

api_article = Blueprint("api_article", __name__)


@api_article.route("/", methods=["GET"])
@limiter.limit("3000 per day")
@limiter.limit("5/seconds")
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
