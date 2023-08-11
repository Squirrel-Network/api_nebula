#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class GroupsFilters(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    exe_filter = fields.BooleanField(default=False)
    gif_filter = fields.BooleanField(default=False)
    jpg_filter = fields.BooleanField(default=False)
    docx_filter = fields.BooleanField(default=False)
    apk_filter = fields.BooleanField(default=False)
    compress_filter = fields.BooleanField(default=False)

    async def get_filters(self):
        return {
            "exe_filter": self.exe_filter,
            "gif_filter": self.gif_filter,
            "jpg_filter": self.jpg_filter,
            "docx_filter": self.docx_filter,
            "apk_filter": self.apk_filter,
            "compress_filter": self.compress_filter,
        }

    class Meta:
        table = "groups_filters"
