from wit import Wit
from settings import WIT_SERVER_TOKEN
import datetime
from dateutil.relativedelta import relativedelta
from constants import ordered_list_of_required_values, independent_wit_intents, default_required_values


class WitExtractor(object):
    def __init__(self, uid, useful_values):
        super(WitExtractor, self).__init__()
        if not useful_values:
            self.useful_values = default_required_values
        else:
            self.useful_values = useful_values
        self.session_id = uid
        self.result = {}
        self.w = Wit(access_token=WIT_SERVER_TOKEN, actions={'send': self.send, "get_context": self.get_context})

    @staticmethod
    def get_updated_date(date, val):
        fmt = "%Y-%m-%d"
        date = datetime.datetime.strptime(date, fmt)
        if val == 'to':
            return date - datetime.timedelta(1)
        return date

    def get_value_from_entity(self, entities, entity):
        entity_data = entities[entity][0]
        if entity == 'datetime':
            if 'value' in entity_data:
                grain = entity_data['grain']
                value = entity_data['value']
                to_date = None
                from_date = self.get_updated_date(value.split("T")[0], 'value')

                if grain == 'day':
                    pass
                elif grain == 'week':
                    to_date = (from_date + relativedelta(weeks=1)) - datetime.timedelta(1)
                elif grain == 'month':
                    to_date = (from_date + relativedelta(months=1)) - datetime.timedelta(1)
                elif grain == 'year':
                    to_date = (from_date + relativedelta(years=1)) - datetime.timedelta(1)

                if to_date is None:
                    to_date = from_date

                self.useful_values['datetime'] = (from_date.strftime('%Y%m%d'), to_date.strftime('%Y%m%d'))
            else:
                self.useful_values['datetime'] = (
                    self.get_updated_date(entity_data['from']['value'].split("T")[0], 'from').strftime('%Y%m%d'),
                    self.get_updated_date(entity_data['to']['value'].split("T")[0], 'to').strftime('%Y%m%d')
                )

        else:
            if 'value' in entity_data:
                self.useful_values[entity] = entity_data['value']
            else:
                self.useful_values[entity] = ''

    def get_wit_response(self, text):
        self.w.run_actions(session_id=self.session_id, message=text)
        return self.result

    def send(self, request, response):
        delete_conversation = False
        if request.get('entities') and request['entities'].get('intent'):
            if request['entities']['intent'][0]['value'] in independent_wit_intents:
                delete_conversation = True
        self.result['delete_conversation'] = delete_conversation
        self.result['response_text'] = response['text']
        self.result['useful_values'] = self.useful_values

    def get_context(self, request):
        context = {}
        entities = request['entities']
        context[self.get_next_param(entities)] = True
        if '' not in self.useful_values.values():
            return self.useful_values
        return context

    def get_next_param(self, entities):
        for i in ordered_list_of_required_values:
            if entities.get(i):
                self.get_value_from_entity(entities, i)

        for key in ordered_list_of_required_values:
            if not self.useful_values[key]:
                return 'missing' + key[0].upper() + key[1:]