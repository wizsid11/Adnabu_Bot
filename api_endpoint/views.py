from __future__ import absolute_import, unicode_literals
import json
import logging

from flask import request, make_response, jsonify, redirect, Flask, render_template

from api_endpoint import slack_bot
from api_endpoint.tasks import slack_event_handler, slack_interactive_action_handler, slack_slash_command_handler
from settings import APP_NAME


app = Flask(APP_NAME)
logger = logging.getLogger(APP_NAME)


@app.route("/success", methods=["GET", "POST"])
def successfully_installed():
    state = request.args.get('state')
    code_arg = request.args.get('code')
    slack_bot.auth(code_arg, state)
    return redirect('https://www.adnabu.com/chatbot/slack/success/'+state)


@app.route("/event", methods=["GET", "POST"])
def events_listener():
    logger.debug('[flask_endpoint] received event - %s' % request.__dict__)
    slack_event = json.loads(request.data)
    logger.info('[flask_endpoint] received event - %s' % slack_event)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if slack_bot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                    %s\n\n" % (slack_event["token"], slack_bot.verification)
        return make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        slack_event_handler.delay(event_type, slack_event)
        return make_response('response', 200)
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/command", methods=["POST"])
def slash_commands_listener():
    slack_command = request.form
    logger.info('[flask_endpoint] received slash command - %s' % slack_command)
    if slack_bot.verification != request.form.get('token'):
        message = "Invalid Slack verification token: %s \npyBot has: \
                    %s\n\n" % (slack_command['token'], slack_bot.verification)
        return make_response(message, 403, {"X-Slack-No-Retry": 1})
    if "command" in slack_command:
        command = slack_command['command']
        slack_slash_command_handler.delay(command, slack_command)
    response = jsonify({
        "response_type": "in_channel"
    })
    return make_response(response, 200)


@app.route("/interactive", methods=["POST"])
def interactive_messages_listener():
    action_data = json.loads(request.form['payload'])
    logger.info('[flask_endpoint] received interactive message - %s' % action_data)
    if slack_bot.verification != action_data['token']:
        message = "Invalid Slack verification token: %s \npyBot has: \
                    %s\n\n" % (action_data['token'], slack_bot.verification)
        return make_response(message, 403, {"X-Slack-No-Retry": 1})
    message_ts = action_data['message_ts']
    slack_interactive_action_handler.delay(action_data, message_ts)
    return make_response("processing", 200, {"content_type": "application/json"})
# test routes


@app.route("/test/install", methods=["GET"])
def test_install():
    client_id = slack_bot.oauth["client_id"]
    scope = slack_bot.oauth["scope"]
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/test/success", methods=["GET", "POST"])
def thanks():
    code_arg = request.args.get('code')
    state = request.args.get('state')
    slack_bot.auth(code_arg, state)
    return render_template("thanks.html")