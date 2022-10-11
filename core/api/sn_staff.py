#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, jsonify
from core.utilities.limiter import limiter
from core.database.repository.users import UserRepository

api_staff_sn = Blueprint('api_staff_sn', __name__)

@api_staff_sn.route('/snstaff', methods=['GET'])
@limiter.limit("2000 per day")
@limiter.limit("3/seconds")
def staff():
    snstaffs = UserRepository().getSnStaff()

    return jsonify(list(map(lambda row: {
        'id': row['id'],
        'name': row['name'],
        'contact': row['contact'],
        'git': row['git'],
        'photo': row['photo']
    }, snstaffs)))