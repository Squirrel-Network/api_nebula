#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

class Config(object):
     ###########################
     ##   DATABASE SETTINGS  ##
     ##########################
     HOST = ''
     PORT = 3306
     USER = ''
     PASSWORD = ''
     DBNAME = ''
     ###########################
     ####   APP SETTINGS    ####
     ##########################
     DEBUG = False
     TOKEN = 'INSERT TOKEN HERE'
     SECRET = 'INSERT APP SECRET HERE'
     TOKEN_DURATION_MINUTES = 30
     ###############################
     ####   TELEGRAM SETTINGS   ####
     ###############################
     BOT_TOKEN = 'INSERT BOT TOKEN HERE'