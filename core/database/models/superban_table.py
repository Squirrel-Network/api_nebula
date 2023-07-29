#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from tortoise import fields
from tortoise.models import Model


class SuperbanTable(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(unique=True)
    user_first_name = fields.CharField(255, default="Unknown")
    motivation_text = fields.CharField(255)
    user_date = fields.DatetimeField(auto_now_add=True)
    id_operator = fields.BigIntField()
    username_operator = fields.CharField(50)
    first_name_operator = fields.CharField(255)

    async def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_first_name": self.user_first_name,
            "motivation_text": self.motivation_text,
            "user_date": self.user_date.isoformat(),
            "id_operator": self.id_operator,
            "username_operator": self.username_operator,
            "first_name_operator": self.first_name_operator,
        }

    class Meta:
        table = "superban_table"
