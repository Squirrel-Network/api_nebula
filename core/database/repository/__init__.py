#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

__all__ = (
    "CommunityRepository",
    "GroupRepository",
    "SuperbanRepository",
    "UserRepository",
)

from .community import CommunityRepository
from .groups import GroupRepository
from .superban import SuperbanRepository
from .users import UserRepository
