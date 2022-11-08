from flask_restful import Resource, request
from flask import Request
from repository import Repository

repository = Repository()


class Event(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo

    def get(self, event_id=None, title=None):
        if event_id is not None:
            return self.repo.get_event_by_id(int(event_id)).__dict__
        if title is not None:
            return self.repo.get_event_by_title(title).__dict__


class EventList(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo

    def get(self):
        return [event.__dict__ for event in self.repo.get_all_events()]

    def post(self, req=request):
        data = req.get_json()
        return self.repo.add_event(data).__dict__

