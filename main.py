#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config, Session
from core.api import auth, blacklist, group, statistics, test, tools, users
from core.database import init_db

# load .env file
load_dotenv()


# Config
conf = Session.config = Config()


# Fastapi instance
app = FastAPI(title="Nebula API", docs_url="/", version="4.0.0")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Start db
init_db(app)


# API EndPoint
app.include_router(auth.auth)
app.include_router(blacklist.api_blacklist, prefix="/v2")
app.include_router(group.api_group, prefix="/v2")
app.include_router(statistics.api_statistics, prefix="/v2")
app.include_router(test.api_test, prefix="/v2")
app.include_router(tools.api_bot_service, prefix="/v2")
app.include_router(users.api_users, prefix="/v2")
