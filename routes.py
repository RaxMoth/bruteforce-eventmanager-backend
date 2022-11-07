from flask_restful import Resource
from repository import Repository


repo = Repository()


class Event(Resource):
    def get(self, event_id=1):
        return {'Events': f'{event_id} works'}


class EventList(Resource):
    def get(self):
        return [event.__dict__ for event in repo.events_get_all()]

