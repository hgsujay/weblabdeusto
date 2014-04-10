"""
WCLOUD_SETTINGS

This file can be used to add new config elements or to override existing ones.

To do so, it needs to be copied to "wcloud_settings.py". If that's done,
the settings here will override those in wcloud_settings_default.py.

If the env var WCLOUD_SETTINGS is defined, then the elements in the file that
it specifies will override these ones.

"""

import os


#################################
# 
# Flask general configuration
# 
DEBUG = True
SECRET_KEY = os.urandom(32)

ADMIN_MAIL = 'weblab@deusto.es'

# If you want to support reCAPTCHA, set this to
# True and provide the credentials
RECAPTCHA_ENABLED = False
RECAPTCHA_PUBLIC_KEY  = 'public key'
RECAPTCHA_PRIVATE_KEY = 'private key'


MAIL_CONFIRMATION_ENABLED = False

DEBUG_UNDEPLOY_ENABLED = True

# 
# We have to use multiple Redis servers (Redis supports by default up to 16 databases,
# and adding more may affect performance)
# 
REDIS_START_PORT=6379 + 1 # So we don't use the 6379
REDIS_DBS_PER_PORT=16

##########################
# 
# DB configuration:
# 
# Both MySQL and PostgreSQL are supported
# 
DB_NAME = 'wcloud'
DB_HOST = '127.0.0.1'


# 
# MySQL
# 
DB_PORT = 3306
DB_USERNAME = 'weblab'
DB_PASSWORD = 'weblab'

# 
# PostgreSQL
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@%s:%d/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME )
# 
# MySQL
# 
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%d/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME )

#############################
#
# Services configuration
# 
WEBLAB_STARTER_PORT  = 1663
APACHE_RELOADER_PORT = 1662
TASK_MANAGER_PORT    = 1661

PUBLIC_URL = 'http://localhost'
DIR_BASE = os.path.expanduser(os.path.join('~', '.weblab')) # home path
ADMINISTRATORS = ('pablo.orduna@deusto.es',)