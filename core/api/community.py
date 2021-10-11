#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import Blueprint, request, jsonify
from core.utilities.limiter import limiter
from core.database.repository.community import CommunityRepository

api_community = Blueprint('api_community', __name__)

@api_community.route('/community', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("5/seconds")
def community():
    return { "status": "Under Construction" }

@api_community.route('/top_community', methods=['GET'])
@limiter.limit("5000 per day")
@limiter.limit("10/seconds")
def top_ten_community():
    rows = CommunityRepository().top_ten_communities()
    return jsonify(list(map(lambda row: {
        'tg_group_id': row['tg_group_id'],
        'tg_group_name': row['group_name'],
        'tg_group_link': row['tg_group_link'],
        'group_photo': row['group_photo'],
        'language': row['language'],
        'chat_type': row['type'],
        'total_users': row['total_users'],
        'total_message': row['counter']
    }, rows)))