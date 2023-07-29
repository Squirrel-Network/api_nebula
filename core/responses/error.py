#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class NotAuthorizedResponse(BaseModel):
    error: str = "Not authorized"
