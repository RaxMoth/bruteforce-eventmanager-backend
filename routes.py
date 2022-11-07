from flask_restful import Resource
from repository import Repository
from flask import request


repo = Repository()


class Event(Resource):
    def get(self, event_id=1):
        return repo.event_get_by_id(int(event_id)).__dict__

    
    def post(self):
        data = request.get_json()
        print(data)
        return repo.event_add(data).__dict__


class EventList(Resource):
    def get(self):
        return [event.__dict__ for event in repo.events_get_all()]

