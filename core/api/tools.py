#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import urllib.parse

from fastapi import APIRouter, Depends
from httpx import AsyncClient

from config import Session
from core.responses.base import GenericResponse, NotAuthorizedResponse
from core.utilities.rate_limiter import RateLimiter
from core.utilities.token_jwt import validate_token

MAIN_URL = "https://api.telegram.org/"

api_bot_service = APIRouter(prefix="/tools", tags=["tools"])
client = AsyncClient()


async def send_message(chat_id: int, text: str):
    text = urllib.parse.quote_plus(text)
    params = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    return await client.get(
        f"{MAIN_URL}bot{Session.config.BOT_TOKEN}/sendmessage", params=params
    )


@api_bot_service.post(
    "/send_message",
    summary="Send message to a specific chat",
    description="Send message to a specific chat",
    dependencies=[
        Depends(RateLimiter(5000, days=1)),
        Depends(RateLimiter(10, 1)),
        Depends(validate_token),
    ],
    responses={
        200: {"model": GenericResponse, "description": "Operation successful"},
        401: {
            "model": NotAuthorizedResponse,
            "description": "Not authorized, invalid or missing token",
        },
    },
)
async def send_message_post(chat_id: int, text: str):
    await send_message(chat_id, text)

    return GenericResponse(status=f"Text: {text} ChatId: {chat_id}")
