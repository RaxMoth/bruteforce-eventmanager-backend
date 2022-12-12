from flask_restful import Resource, request
from flask import Request

import firebase_admin
from firebase_admin import credentials, auth
from repository import Repository
from flask import request
# from app import get_auth

repository = Repository()
# cred = credentials.Certificate("firebase_admin/hub-roitraining1-poc-93c5-firebase-adminsdk-i8yqn-e656698e4b.json")
# auth_app = firebase_admin.initialize_app(cred)

class Event(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo
        self.uid = request.headers.get("Authorization").split(' ')[1]

    def get(self, event_id=None, title=None, req=request):
        # if request.endpoint == 'get_#likes':
        #     print("getting number of likes")
        #     event = self.repo.get_likes(int(event_id))

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


    def put(self, req=request):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("User verified")
            data = req.get_json()
            event = self.repo.update_event(data)
            return event.__dict__
        except firebase_admin._auth_utils.InvalidIdTokenError as e:
            print('User unable to be verified.')
            print(e)



    def delete(self, event_id):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("User verified")
            self.repo.delete_event(event_id, decoded_token['user_id'])
        except firebase_admin._auth_utils.InvalidIdTokenError as e:
            print('User unable to be verified.')
            print(e)
            return 'User unable to be verified'

    def post(self, req=request):
        data = req.get_json()
        if request.endpoint == 'like_event':
            event = self.repo.like_event(data)
            return event.__dict__


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
        # print(request.headers)
        self.uid = request.headers.get('Authorization').split(' ')[1]

    def get(self):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("Loading all events...")
            return [event.__dict__ for event in self.repo.get_all_events()]
        except firebase_admin._auth_utils.InvalidIdTokenError as e:
            print('User unable to be verified.')
            print(e)
            return 'User unable to be verified'

    def post(self, req=request):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("Creating new event...")
            print("User ID: ", decoded_token['uid'])
            data = req.get_json()
            return self.repo.add_event(data, decoded_token['uid']).__dict__
        except:
            print('User unable to be verified.')
            print("some error")
            return 'User unable to be verified'

