#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from dotenv import load_dotenv
from fastapi import FastAPI

from config import Config, Session
from core.api import auth, blacklist, statistics, users
from core.database import init_db

# load .env file
load_dotenv()


# Config
conf = Session.config = Config()


# Fastapi instance
app = FastAPI(title="Nebula API", docs_url="/", version="3.0.0")


# Start db
init_db(app)


# API EndPoint
app.include_router(auth.auth)
app.include_router(blacklist.api_blacklist)
app.include_router(statistics.api_statistics)
app.include_router(users.api_users)
