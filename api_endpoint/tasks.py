from __future__ import absolute_import, unicode_literals
import logging
import re
from api_endpoint import cache, slack_bot
from core.celery import celery_app
from .functions import get_user, get_api_from_values, get_wit_response, bot_action, check_if_bot
from core.models import SlackAuthedTeam
import requests
import json
from settings import APP_NAME


logger = logging.getLogger(APP_NAME)


@celery_app.task()
def slack_event_handler(event_type, event):
    if event_type != "message":
        return

    user_id = get_user(event)
    if not user_id or check_if_bot(user_id):
        return

    logger.info('[event_handler] received event from user %s' % user_id)
    team_id = event["team_id"]
    access_token = SlackAuthedTeam.get_access_token(team_id)
    channel_id = event["event"]["channel"]
    result = get_wit_response(event["event"]["text"], user_id)
    bot_action('event', user_id, result, access_token, channel_id, team_id)
    return None


@celery_app.task()
def slack_slash_command_handler(command_type, command):
    if command_type != "/adnabubot":
        return
    logger.info('[slash_command_handler] received slash command %s' % command)
    team_id = command["team_id"]
    channel_id = command["channel_id"]
    response_url = command["response_url"]
    access_token = SlackAuthedTeam.get_access_token(team_id)
    result = get_wit_response(command['text'], channel_id)
    bot_action('slash_command', channel_id, result, access_token, channel_id, team_id, response_url)
    return None


@celery_app.task()
def slack_interactive_action_handler(action_data, message_ts):
    account_id = action_data["actions"][0]["name"]
    team_id = action_data["team"]["id"]
    channel_id = action_data["channel"]["id"]
    if channel_id[0] == 'D':
        session_id = action_data["user"]["id"]
    else:
        session_id = channel_id

    data = cache.get(session_id)
    useful_values = json.loads(data)
    api_url = get_api_from_values(useful_values)
    from_date, to_date = useful_values['datetime']
    data = {'adnabu_token': SlackAuthedTeam.get_adnabu_token(team_id), 'account_id': account_id,
            'from_date': from_date, 'to_date': to_date, 'level': useful_values['level']}
    output = requests.post(api_url, data=data)
    filename = re.findall("filename=(.+)", output.headers['content-disposition'])
    cache.delete(session_id)
    access_token = SlackAuthedTeam.get_access_token(team_id)
    slack_bot.update(message_ts, channel_id, access_token)
    slack_bot.send_report(output.text, filename[0], channel_id, access_token)
    return None
