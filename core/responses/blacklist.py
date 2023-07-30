#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class BlacklistUser(BaseModel):
    id: int
    user_id: int
    user_first_name: str
    motivation_text: str
    user_date: str
    id_operator: int
    username_operator: str
    first_name_operator: str


class GetListBlacklistResponse(BaseModel):
    results: list[BlacklistUser]
    total_page: int


class GetBlacklistUserResponse(BlacklistUser):
    pass


class UserNotFound(BaseModel):
    error: str = "The user was not superbanned or you entered an incorrect id"


class AddBlacklistUserPayload(BaseModel):
    user_id: int
    user_first_name: str
    motivation_text: str
    id_operator: int
    username_operator: str
    first_name_operator: str
