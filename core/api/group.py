#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, request
from jsonschema import Draft7Validator

from core.database.repository.groups import GroupRepository
from core.decorators import auth_telegram
from core.utilities.limiter import limiter
from core.utilities.telegram_auth import InitDataModel

FILTERS_KEY = [
    GroupRepository.EXE_FILTER,
    GroupRepository.GIF_FILTER,
    GroupRepository.ZIP_FILTER,
    GroupRepository.TARGZ_FILTER,
    GroupRepository.JPG_FILTER,
    GroupRepository.DOCX_FILTER,
    GroupRepository.APK_FILTER,
]
FILTERS_POST_SCHEMA = Draft7Validator(
    {
        "type": "object",
        "properties": {x: {"type": "boolean"} for x in FILTERS_KEY},
        "required": FILTERS_KEY,
    }
)

api_group = Blueprint("api_group", __name__)


@api_group.route("/group/<chat_id>/filters", methods=["GET"])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth_telegram
def get_filters_settings(chat_id: str, init_data: InitDataModel):
    with GroupRepository() as db:
        data = db.get_by_id(int(chat_id))

    if not data:
        return ({"error": "chat_id does not exist"}, 404)

    return {k: bool(v) for k, v in data.items() if k in FILTERS_KEY}


@api_group.route("/group/<chat_id>/filters", methods=["POST"])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth_telegram
def get_filters_settings_post(chat_id: str, init_data: InitDataModel):
    body = request.json

    if not FILTERS_POST_SCHEMA.is_valid(body):
        return ({"error": "body not correct"}, 400)

    with GroupRepository() as db:
        for k, v in body.items():
            db.update_groups_settings(k, int(v), chat_id)

    return {}
