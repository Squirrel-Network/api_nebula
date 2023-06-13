#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint

from core.database.repository.groups import GroupRepository
from core.utilities.limiter import limiter
from core.decorators import auth_telegram

FILTERS_KEY = [
    GroupRepository.EXE_FILTER,
    GroupRepository.GIF_FILTER,
    GroupRepository.ZIP_FILTER,
    GroupRepository.TARGZ_FILTER,
    GroupRepository.JPG_FILTER,
    GroupRepository.DOCX_FILTER,
    GroupRepository.APK_FILTER,
]

api_group = Blueprint("api_group", __name__)


@api_group.route("/<int:chat_id>/filters", methods=["GET"])
@limiter.limit("5000 per day")
@limiter.limit("5/seconds")
@auth_telegram
def get_filters_settings(chat_id: int):
    with GroupRepository() as db:
        data = db.get_by_id(chat_id)

    if not data:
        return ({"error": "chat_id does not exist"}, 404)

    return {k: v for k, v in data.items() if k in FILTERS_KEY}
