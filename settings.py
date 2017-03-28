# Wit settings
WIT_SERVER_TOKEN = "B6B27XKIJ5JPOTGHG5YAFNZD2RWTXPQZ"

# DB settings
DB_NAME = 'AuthedTeams'
DB_HOST = 'localhost:27017'

# slack configs
SLACK_BOT_ID = "U3L0VM6MD"
SLACK_CLIENT_ID = "3504198033.121408224548"
SLACK_CLIENT_SECRET = "af565dd27001a01d48a50c36f5b7deb6"
SLACK_VERIFICATION_TOKEN = "lorrNkgD82MSRDdU7dgentdL"
SLACK_SCOPES = "commands,bot"
SLACK_BOT_NAME = "adnabu_test_bot"

# cache settings
CACHE_URL = 'redis://localhost:6379/1'

# Celery configs
broker_url = 'redis://localhost:6379/0'
include = ['api_endpoint.tasks']

DEBUG = False

APP_NAME = 'chatbot'

try:
    from local_settings import *
except ImportError:
    pass