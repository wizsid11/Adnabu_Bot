import logging
from api_endpoint import slack_bot, cache
from settings import SLACK_BOT_ID, APP_NAME
from wit_controller.wit_extract import WitExtractor
import json
import requests
from core.models import SlackAuthedTeam


logger = logging.getLogger(APP_NAME)


def get_wit_response(text, session_id):
    data = cache.get(session_id)
    useful_values = None
    if data:
        useful_values = json.loads(data)
    conversation = WitExtractor(session_id, useful_values)
    result = conversation.get_wit_response(text)
    logger.info('[get_wit_response] wit result for text "%s" and session id %s - %s' % (text, session_id, result))
    return result


def get_user(slack_event):
    if 'user' in slack_event['event']:
        user_id = slack_event['event']['user']
        return user_id
    return None


def check_if_bot(user_id):
    return user_id == SLACK_BOT_ID


def bot_action(action, session_id, result, access_token, channel_id, team_id, response_url=None):
    logger.info('[bot_action] received action %s and result %s' % (action, result))
    if result['delete_conversation']:
        if cache.get(session_id):
            cache.delete(session_id)
    else:
        cache.set(session_id, json.dumps(result['useful_values']))
        if '' not in result['useful_values'].values():
            try:
                output = requests.post("https://www.adnabu.com/chatbot/get/accounts",
                                       data={'adnabu_token': SlackAuthedTeam.get_adnabu_token(team_id)})
                accounts = json.loads(output.text)
                slack_bot.send_button(access_token, channel_id, accounts)
            except Exception as e:
                logger.error('[bot_action] failed to fetch accounts for team id %s' % team_id)
            return

    if action == 'event':
        slack_bot.send_event_response(result, access_token, channel_id)
    elif action == 'slash_command':
        slack_bot.send_slash_response(result, response_url)


def get_api_from_values(values):
    mapping = ((('format', ['report']), 'https://www.adnabu.com/chatbot/fetch/report'),
               (('format', ['graph']), 'https://www.adnabu.com/chatbot/fetch/graph'))
    for item in mapping:
        for i in range(len(item)-1):
            if values[item[i][0].strip()].strip() != item[i][1][0]:
                break
            return item[len(item)-1]