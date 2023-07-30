#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class TopGroup(BaseModel):
    counter: int
    group_name: str
    group_photo: str
    language: str
    tg_group_id: int
    tg_group_link: str
    total_users: int
    type: str


class GroupsTopTenResponse(BaseModel):
    results: list[TopGroup]
