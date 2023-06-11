#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import urllib.request

import requests
from flasgger import swag_from
from flask import Blueprint, request

from config import Session
from core.decorators import auth_required
from core.utilities.limiter import limiter

api_bot_service = Blueprint("api_bot_service", __name__)

MAIN_URL = "https://api.telegram.org/"


def ApiMessage(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = MAIN_URL + "bot{}/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(
        Session.config.BOT_TOKEN, chat_id, text
    )
    send = requests.get(url)
    return send


@api_bot_service.route("/SendMessage", methods=["POST"])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
@auth_required
@swag_from("../../openapi/message_post.yaml")
def send_message():
    message = request.args.get("text")
    chat_id = request.args.get("chatid")
    if not (message and chat_id):
        return {"error": "Missing text and chatid params"}, 400
    ApiMessage(message, chat_id)
    return {"status": "Text: {} ChatId: {}".format(message, chat_id)}
