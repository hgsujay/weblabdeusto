# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals,
# listed below:
#
# Author: Xabier Larrakoetxea <xabier.larrakoetxea@deusto.es>
# Author: Pablo Orduña <pablo.orduna@deusto.es>
#
# These authors would like to acknowledge the Spanish Ministry of science
# and innovation, for the support in the project IPT-2011-1558-430000
# "mCloud: http://innovacion.grupogesfor.com/web/mcloud"
#

import os

#Flask configuration
DEBUG = True
SECRET_KEY = 'development key'

ADMIN_MAIL = 'weblab@deusto.es'

# DB configuration


DB_NAME = 'wcloud'
DB_HOST = '127.0.0.1'
# 
# PostgreSQL
# DB_PORT = 5432
# DB_USERNAME = 'postgres'
# DB_PASSWORD = 'postgres'
# 
# MySQL
# 
DB_PORT = 3306
DB_USERNAME = 'weblab'
DB_PASSWORD = 'weblab'

# 
# Services configuration
WEBLAB_STARTER_PORT  = 1663
APACHE_RELOADER_PORT = 1662
TASK_MANAGER_PORT    = 1661

PUBLIC_URL = 'http://localhost'
DIR_BASE = os.path.expanduser(os.path.join('~', '.weblab')) # home path

# 
# PostgreSQL
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@%s:%d/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME )
# 
# MySQL
# 
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%d/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME )

