#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import Config, Session
from core.database import init_db
from core.database.models import SuperbanTable, Users
from core.utilities.functions import get_formatted_time

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
@app.get("/")
async def index(request: Request):
    data = SuperbanTable.all()
    last_super_banned = await data.order_by("-user_date").limit(8).values()
    count_super_banned = await data.count()

    for row in last_super_banned:
        row["upper"] = row["user_first_name"][:1].upper()
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
@app.route("/users", methods=["GET", "POST"])
@app.route("/users/<username>", methods=["GET"])
def users_search(username: str = None):
    if request.method == "POST":
        username = request.form.get("username").strip().lower()

    with UserRepository() as db:
        counter = db.get_count_users()
        data = db.get_by_username(username)

    return render_template("users.html", data=data, counter=counter["counter"])


# Fake Route
@app.get("/wp-admin")
@app.get("/wp-login")
@app.get("/admin")
async def fake_route(request: Request):
    return templates.TemplateResponse("fakeroute.html", {"request": request})
