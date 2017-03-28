import settings
from core.models import SlackAuthedTeam
import json
import requests
from slackclient import SlackClient
from functions import generate_accounts_attachments


class Bot(object):
    def __init__(self):
        super(Bot, self).__init__()
        self.name = settings.SLACK_BOT_NAME
        self.oauth = {"client_id": settings.SLACK_CLIENT_ID,
                      "client_secret": settings.SLACK_CLIENT_SECRET,
                      "scope": settings.SLACK_SCOPES}
        self.verification = settings.SLACK_VERIFICATION_TOKEN
        self.client = SlackClient("")

    def auth(self, code, state):
        auth_response = self.client.api_call("oauth.access",
                                             client_id=self.oauth["client_id"],
                                             client_secret=self.oauth["client_secret"],
                                             code=code)
        team_id = auth_response["team_id"]
        SlackAuthedTeam.add_authed_team(team_id, auth_response["bot"]["bot_access_token"], state)

    def send_event_response(self, result, access_token, channel):
        self.client = SlackClient(access_token)
        self.client.api_call("chat.postMessage", channel=channel, text=result['response_text'])

    def update(self, message_ts, channel, access_token):
        self.client = SlackClient(access_token)
        self.client.api_call("chat.update", channel=channel, text="Here you Go!", ts=message_ts)

    def send_report(self, content, filename, channel, access_token):
        self.client = SlackClient(access_token)
        self.client.api_call("files.upload", channels=channel, content=content, filename=filename)

    @staticmethod
    def send_slash_response(result, response_url):
        headers = {'Content-Type': 'application/json'}
        data = {'text': result['response_text'], 'response_type': 'in_channel'}
        requests.post(response_url, data=json.dumps(data), headers=headers)

    def send_button(self, access_token, channel, accounts):
        self.client = SlackClient(access_token)
        self.client.api_call("chat.postMessage", channel=channel,
                             attachments=generate_accounts_attachments(accounts.items()))
