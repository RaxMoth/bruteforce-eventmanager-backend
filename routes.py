from flask_restful import Resource, request
from flask import Request
from repository import Repository
from flask import request

repository = Repository()


class Event(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo

    def get(self, event_id=None, title=None):
        if event_id is not None:
            event = self.repo.get_event_by_id(int(event_id))
            if event is None:
                return {"idError": f"Event with the id {event_id} not found"}
            return event.__dict__
        if title is not None:
            event = self.repo.get_event_by_title(title)
            if event is None:
                return {"titleError": f"Event with the title {title} not found"}
            return event.__dict__

    def put (self, req = request):
        data = req.get_json()
        event = self.repo.update_event(data)
        return event.__dict__

    def delete (self, event_id):
        self.repo.delete_event(event_id)

class User(Resource):

    def __init__(self, repo=Repository()):
        self.repo = repo

    def get(self, username):
        if username is not None:
            user = self.repo.get_user_by_id(username)
            if user is None:
                return {"idError": f"Event with the id {username} not found"}
            return user.__dict__

    def post(self, req=request):
        data = req.get_json()
        return self.repo.add_user(data).__dict__


class EventList(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo

    def get(self):
        return [event.__dict__ for event in self.repo.get_all_events()]

    def post(self, req=request):
        data = req.get_json()
        return self.repo.add_event(data).__dict__
