#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class TokenPayload(BaseModel):
    token: str


class AuthResponse(BaseModel):
    token: str


class ErrorMissingToken(BaseModel):
    error: str = "Missing token"


class ErrorNotAuthorized(BaseModel):
    error: str = "Not authorized"
