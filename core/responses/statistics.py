#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class TopGroup(BaseModel):
    tg_group_id: int
    tg_group_name: str
    total_message: int


class TopCommunity(BaseModel):
    chat_type: str
    group_photo: str
    language: str
    tg_group_id: int
    tg_group_link: str
    tg_group_name: str
    total_message: int
    total_users: int


class GroupsTopTenResponse(BaseModel):
    results: list[TopGroup]


class CommunityTopTenResponse(BaseModel):
    results: list[TopCommunity]
