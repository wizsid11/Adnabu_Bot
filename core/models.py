from pymongo import MongoClient
from settings import DB_HOST, DB_NAME


class Collection(object):
    collection_name = None
    db = None

    @staticmethod
    def get_db():
        client = MongoClient(DB_HOST)
        db = client[DB_NAME]
        return db

    @classmethod
    def insert(cls, row):
        return cls.get_db()[cls.collection_name].insert(row)

    @classmethod
    def find(cls, row):
        return cls.get_db()[cls.collection_name].find(row)

    @classmethod
    def find_one(cls, row):
        return cls.get_db()[cls.collection_name].find_one(row)

    class Meta:
        abstract = True

    def __init__(self):
        super(Collection, self).__init__()
        if not self.collection_name:
            raise NotImplementedError('Need to specify a collection name')
        self.get_db()


class SlackAuthedTeam(Collection):
    collection_name = 'Slack_Authed_Team_Access_Token'

    @classmethod
    def add_authed_team(cls, team_id, access_token, state):
        cls.insert({'team_id': team_id, 'access_token': access_token, 'adnabu_token': state})

    @classmethod
    def get_all_authed_teams(cls):
        cursor = cls.find({})
        results = []
        for x in cursor:
            results.append(x['team_id'])
        return results

    @classmethod
    def get_access_token(cls, team_id):
        result = cls.find_one({'team_id': team_id})
        return result['access_token']

    @classmethod
    def get_adnabu_token(cls,team_id):
        result = cls.find_one({'team_id': team_id})
        return result['adnabu_token']