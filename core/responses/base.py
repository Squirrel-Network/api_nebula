#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from pydantic import BaseModel


class GenericError(BaseModel):
    error: str = ""


class NotAuthorizedResponse(GenericError):
    error: str = "Not authorized"


class GenericResponse(BaseModel):
    status: str
