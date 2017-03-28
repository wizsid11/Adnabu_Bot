from wit_extract import WitExtractor

responses = {"missing_datetime": "Please specify a duration",
             "missing_level": "campaign or adgroup or accounts?",
             "missing_format": "Do you want a report or a graph?",
             "finish": "Here you go!",
             "bye": "Bye Bye",
             "greeting": "Hey! What can i do for you?"}

#todo Have to write new test cases for git_response after changes in wit


def test_get_wit_response():
    tester1 = WitExtractor("testing", None)
    tester1.get_wit_response("Bye")
    assert tester1.result['response_text'] == responses["bye"]
    tester1.get_wit_response("Can i see my report for last month")
    assert tester1.result['response_text'] == responses["missing_level"]
    tester1.get_wit_response("campaign")
    assert tester1.result['response_text'] == responses['finish']
    tester2 = WitExtractor("testing", None)
    tester2.get_wit_response("Hello")
    assert tester2.result['response_text'] == responses["greeting"]
    tester2.get_wit_response("I want to check my reports")
    assert tester2.result['response_text'] == responses["missing_datetime"]
    tester2.get_wit_response("last month")
    assert tester2.result['response_text'] == responses["missing_level"]
    tester2.get_wit_response("last three months")
    assert tester2.result['response_text'] == responses["missing_level"]
    tester2.get_wit_response("campaign")
    assert tester2.result['response_text'] == responses['finish']
    tester3 = WitExtractor("testing", None)
    tester3.get_wit_response("campaign")
    assert tester3.result['response_text'] == responses["missing_datetime"]
    tester3.get_wit_response("report for last month")
    assert tester3.result['response_text'] == responses['finish']


def test_get_updated_date():
    date = WitExtractor.get_updated_date("2016-11-01", 'value')
    assert str(date) == "2016-11-01 00:00:00"
    date = WitExtractor.get_updated_date("2016-09-01", 'from')
    assert str(date) == "2016-09-01 00:00:00"
    date = WitExtractor.get_updated_date("2016-12-01", 'to')
    assert str(date) == "2016-11-30 00:00:00"


def test_get_value_from_entity():
    tester = WitExtractor("testing", None)
    tester.get_value_from_entity({'format': [{'value': 'report'}]}, 'format')
    assert tester.useful_values == {'datetime': '', 'level': '', 'format': 'report'}
    tester.get_value_from_entity({'datetime': [{'grain': "month", "value": "2016-09-01T00:00.000-07:00"}]}, 'datetime')
    assert tester.useful_values == {'datetime': ('2016-09-01 00:00:00', '2016-09-30 00:00:00'), 'level': '', 'format': 'report'}
    tester.get_value_from_entity({'level': [{'value': 'campaign'}]}, 'level')
    assert tester.useful_values == {'datetime': ('2016-09-01 00:00:00', '2016-09-30 00:00:00'), 'level': 'campaign', 'format': 'report'}


def test_get_next_params():
    tester = WitExtractor("testing", None)
    missing_entity = tester.get_next_param(({'format': [{'value': 'graph'}]}))
    assert missing_entity == "missingDatetime"
    tester = WitExtractor("testing", {})
    missing_entity = tester.get_next_param({'format': [{'value': 'graph'}]})
    assert missing_entity == "missingDatetime"
    missing_entity = tester.get_next_param({'datetime': [{'grain': "month", "value": "2016-09-01T00:00.000-07:00"}]})
    assert missing_entity == "missingLevel"
