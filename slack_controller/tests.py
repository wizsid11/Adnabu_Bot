__author__ = 'wizsid'
from functions import generate_accounts_attachments

test_dict = {}
attachments = [{'callback_id': 'something', 'text': 'Choose a account',
                'actions': [{'text': 'account0', 'type': 'button', 'name': '0', 'value': '0'},
                            {'text': 'account1', 'type': 'button', 'name': '1', 'value': '1'},
                            {'text': 'account10', 'type': 'button', 'name': '10', 'value': '10'}]},
               {'callback_id': 'something', 'text': '',
                'actions': [{'text': 'account2', 'type': 'button', 'name': '2', 'value': '2'},
                            {'text': 'account3', 'type': 'button', 'name': '3', 'value': '3'},
                            {'text': 'account4', 'type': 'button', 'name': '4', 'value': '4'}]},
               {'callback_id': 'something', 'text': '',
                'actions': [{'text': 'account5', 'type': 'button', 'name': '5', 'value': '5'},
                            {'text': 'account6', 'type': 'button', 'name': '6', 'value': '6'},
                            {'text': 'account7', 'type': 'button', 'name': '7', 'value': '7'}]},
               {'callback_id': 'something', 'text': '',
                'actions': [{'text': 'account8', 'type': 'button', 'name': '8', 'value': '8'},
                            {'text': 'account9', 'type': 'button', 'name': '9', 'value': '9'}]}]

for i in range(11):
    test_dict[str(i)] = "account%s" % i


def test_generate_attachments():
    assert generate_accounts_attachments(test_dict.items()) == attachments

