#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class User(BaseModel):
    id: int
    tg_id: int
    tg_username: str
    created_at: str
    updated_at: str


class GetUsersResponse(BaseModel):
    results: list[User]
    total_page: int


class GetUserByIdResponse(User):
    pass


class UserNotExistErrorModel(BaseModel):
    error: str = (
        "You have entered an id that does not exist or you have entered incorrect data"
    )
