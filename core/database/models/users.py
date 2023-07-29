#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    tg_username = fields.CharField(50)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def to_dict(self):
        return {
            "id": self.id,
            "tg_id": self.tg_id,
            "tg_username": self.tg_username,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    class Meta:
        table = "users"
