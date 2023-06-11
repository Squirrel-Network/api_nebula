#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, jsonify

from core.database.repository import UserRepository
from core.utilities.limiter import limiter

api_staff_sn = Blueprint("api_staff_sn", __name__)


@api_staff_sn.route("/", methods=["GET"])
@limiter.limit("2000 per day")
@limiter.limit("3/seconds")
def staff():
    with UserRepository() as db:
        snstaffs = db.get_sn_staff()

    return jsonify(snstaffs)
