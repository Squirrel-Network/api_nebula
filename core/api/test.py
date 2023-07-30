#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from fastapi import APIRouter, Depends

from core.responses.base import GenericResponse
from core.utilities.rate_limiter import RateLimiter

api_test = APIRouter(prefix="/hi", tags=["general"])


@api_test.get(
    "/",
    summary="Hi function",
    description="Hi function",
    dependencies=[
        Depends(RateLimiter(1000, days=1)),
        Depends(RateLimiter(3, 1)),
    ],
    responses={
        200: {"model": GenericResponse, "description": "Hi response"},
    },
)
async def hi():
    return GenericResponse(status="hi!")
