from api_endpoint.tasks import get_user
import random


request_for_test_get_user = {
    'yes_user': [{"token": "ubmwBQFLljKjg4kyuRyKirhv", "team_id": "T03EU5U0Z", "api_app_id": "A3C4K7Q9Y",
                  "event": {"type": "message", "user": "something", "text": '',
                            "ts": "1481723029.000024", "channel": "something", "event_ts": "1481723029.000024"},
                  "type": "event_callback", "authed_users": ["U3C7RPMQV"]}, "something"],
    'no_user': [{"token": "ubmwBQFLljKjg4kyuRyKirhv", "team_id": "T03EU5U0Z", "api_app_id": "A3C4K7Q9Y",
                 "event": {"text": "", "username": "Adnabu Bot", "bot_id": "B3C56Q5T4",
                           "type": "message", "subtype": "bot_message", "ts": "1481786454.000010",
                           "channel": "D3C7FBH6Y", "event_ts": "1481786454.000010"},
                 "type": "event_callback",
                 "authed_users": ["U3C7RPMQV"]}, None]}


def test_get_user():
    for i in range(5):
        random_key = random.sample(request_for_test_get_user, 1)[0]
        slack_event = request_for_test_get_user[random_key][0]
        actual_user = request_for_test_get_user[random_key][1]
        assert get_user(slack_event) == actual_user

