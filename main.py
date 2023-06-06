#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import os
from datetime import datetime

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS

from config import Config, Session
from core.api import (
    article,
    auth,
    blacklist,
    bot_service,
    community,
    groups,
    sn_staff,
    test,
    users,
)
from core.database import create_pool
from core.database.repository import SuperbanRepository, UserRepository
from core.utilities.functions import get_formatted_time
from core.utilities.limiter import limiter

# load .env file
load_dotenv()


# Config
conf = Session.config = Config()


# Load pool
Session.db_pool = create_pool()


# load Flask
app = Flask(__name__)
app.config.from_object(conf)
# Enable CORS Policy
CORS(app)

limiter.init_app(app)


Swagger(
    app,
    template_file="./openapi/main.yaml",
    merge=True,
    config={
        "title": "Nebula API specs",
        "openapi": "3.0.0",
        "specs": [{"endpoint": "openapi/specs", "route": "/openapi/specs.json"}],
    },
)


# Home
@app.route("/")
def index():
    with SuperbanRepository() as db:
        data = db.get_last_super_banned()
        countsb = db.get_count_super_banned()

    for row in data:
        row["upper"] = row["user_first_name"][:1].upper()
        row["user_time"] = get_formatted_time(str(row["user_date"]))

    countsbNm = "{:20,}".format(countsb["counter"])
    time_in_utc = datetime.utcnow()
    now_time = time_in_utc.strftime("%b %d %Y %H:%M %Z")

    return render_template("home.html", data=data, countsb=countsbNm, now_time=now_time)


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
@app.route("/wp-admin", methods=["POST", "GET"])
@app.route("/wp-login", methods=["POST", "GET"])
@app.route("/admin", methods=["POST", "GET"])
def fake_route():
    return render_template("fakeroute.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


# API EndPoint
app.register_blueprint(auth.auth, url_prefix="/authenticate")
app.register_blueprint(test.api_test, url_prefix="/v1/hi")
app.register_blueprint(blacklist.api_blacklist, url_prefix="/v1")
app.register_blueprint(users.api_users, url_prefix="/v1")
app.register_blueprint(community.api_community, url_prefix="/v1")
app.register_blueprint(groups.api_groups, url_prefix="/v1")
app.register_blueprint(bot_service.api_bot_service, url_prefix="/v1")
app.register_blueprint(article.api_article, url_prefix="/v1/news")
app.register_blueprint(sn_staff.api_staff_sn, url_prefix="/v1/snstaff")


if __name__ == "__main__":
    app.run(debug=conf.DEBUG, host="localhost")
