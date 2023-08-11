#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class GroupFilters(BaseModel):
    exe_filter: bool
    gif_filter: bool
    jpg_filter: bool
    docx_filter: bool
    apk_filter: bool
    compress_filter: bool


class GetGroupInfo(BaseModel):
    chat_id: int
    group_name: str
    language: str
    max_warn: int
    total_users: int
    total_messages: int
    group_photo: str


class GetGroupFilters(GroupFilters):
    pass


class ChangeGroupFiltersPayload(GroupFilters):
    pass
