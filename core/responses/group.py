#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class GroupFilters(BaseModel):
    exe_filter: bool
    gif_filter: bool
    zip_filter: bool
    targz_filter: bool
    jpg_filter: bool
    docx_filter: bool
    apk_filter: bool


class GetGroupFilters(GroupFilters):
    pass


class ChangeGroupFiltersPayload(GroupFilters):
    pass
