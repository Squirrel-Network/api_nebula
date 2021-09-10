#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#Limit Request
limiter = Limiter(
    None,
    key_func=get_remote_address,
    default_limits=["300 per minute", "10 per second"],
)
