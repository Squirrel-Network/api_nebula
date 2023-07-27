#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import Config, Session
from core.database import init_db
from core.database.models import SuperbanTable, Users
from core.utilities.functions import get_formatted_time
from core.api import auth

# load .env file
load_dotenv()


# Config
conf = Session.config = Config()


# Fastapi instance
app = FastAPI(title="Nebula API")
app.mount("/static", StaticFiles(directory="static"), "static")


# Templates
templates = Jinja2Templates(directory="templates")


# Start db
init_db(app)


# Home
@app.get("/", include_in_schema=False)
async def index(request: Request):
    data = SuperbanTable.all()
    last_super_banned = await data.order_by("-user_date").limit(8).values()
    count_super_banned = await data.count()

    for row in last_super_banned:
        row["upper"] = row["user_first_name"][0].upper()
        row["user_time"] = get_formatted_time(str(row["user_date"]))

    time_in_utc = datetime.utcnow()
    now_time = time_in_utc.strftime("%b %d %Y %H:%M %Z")

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "data": last_super_banned,
            "now_time": now_time,
            "countsb": count_super_banned,
        },
    )


# User Search
@app.get("/users", include_in_schema=False)
@app.get("/users/{username}", include_in_schema=False)
async def users_search(request: Request, username: str = None):
    counter = await Users.all().count()
    data = await Users.get_or_none(tg_username=username).values()

    return templates.TemplateResponse(
        "users.html", {"request": request, "data": data, "counter": counter}
    )


@app.post("/users", include_in_schema=False)
async def users_search_post(request: Request, username: str = Form()):
    counter = await Users.all().count()
    data = await Users.get_or_none(tg_username=username)

    if data:
        data.created_at = data.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data.updated_at = data.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse(
        "users.html", {"request": request, "data": data, "counter": counter}
    )


# Fake Route
@app.get("/wp-admin", include_in_schema=False)
@app.get("/wp-login", include_in_schema=False)
@app.get("/admin", include_in_schema=False)
async def fake_route(request: Request):
    return templates.TemplateResponse("fakeroute.html", {"request": request})


# API EndPoint
app.include_router(auth.auth)
