__author__ = 'wizsid'


def generate_accounts_attachments(accounts):
        attachments = []
        group_size = 3
        sorted_accounts = sorted(accounts, key=lambda t: t[1])
        for i in range(len(sorted_accounts) / group_size + 1):
            actions = map(lambda a: {"name": a[0], "text": a[1], "type": "button", "value": a[0]},
                          sorted_accounts[i * group_size:(i + 1) * group_size])
            text = 'Choose a account' if i == 0 else ''
            attachments.append({'text': text, "callback_id": "something", "actions": actions})
        return attachments