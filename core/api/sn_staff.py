#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

from flask import Blueprint, jsonify
from quart_rate_limiter import rate_limit

from core.database.repository import UserRepository

api_staff_sn = Blueprint("api_staff_sn", __name__)


@api_staff_sn.route("/", methods=["GET"])
@rate_limit(2000, datetime.timedelta(days=1))
@rate_limit(3, datetime.timedelta(seconds=1))
def staff():
    with UserRepository() as db:
        snstaffs = db.get_sn_staff()

    return jsonify(snstaffs)
