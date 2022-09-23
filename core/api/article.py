#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint, request, jsonify
from core.utilities.limiter import limiter
from core.utilities.functions import format_iso_date
from core.database.repository.groups import GroupRepository

api_article = Blueprint('api_article', __name__)

@api_article.route('/news', methods=['GET'])
@limiter.limit("2000 per day")
@limiter.limit("3/seconds")
def article():
    articles = GroupRepository().get_article()
    return jsonify(list(map(lambda row: {
        'article_id': row['article_id'],
        'language': row['language'],
        'content': row['content'],
        'created_at': format_iso_date(row['created_at']),
        'updated_at': format_iso_date(row['updated_at'])
    }, articles)))


