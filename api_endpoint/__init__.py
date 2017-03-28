import redis
from settings import CACHE_URL
from slack_controller import bot

cache = redis.StrictRedis.from_url(CACHE_URL)
slack_bot = bot.Bot()