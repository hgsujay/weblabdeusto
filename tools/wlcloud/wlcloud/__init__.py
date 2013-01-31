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

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)

#Config
app.config.from_object(settings)

#Extensions
db = SQLAlchemy(app)

#Import before use because we need to create the databases and to manage without running the webapp
import wlcloud.models

import wlcloud.views
