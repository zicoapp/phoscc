# coding: utf-8
import os


class Config(object):
    """Base config class."""
    # Flask app config
    DEBUG = False
    TESTING = False
    SECRET_KEY = "CxxsLDSDnNdxxSSWDMlsd98xSqp"
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    SESSION_COOKIE_NAME = 'phoscc_session'

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Site domain
    SITE_TITLE = "yuntu"
    SITE_DOMAIN = "http://yuntu.com:3000"

    # SQLAlchemy config
    # See:
    # https://pythonhosted.org/Flask-SQLAlchemy/config.html#connection-uri-format
    # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@host/database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-DebugToolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Sentry config
    SENTRY_DSN = ''

    # Host string, used by fabric
    HOST_STRING = "root@12.34.56.78"
