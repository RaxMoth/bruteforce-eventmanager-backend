from flask_restful import Resource, request
from flask import Request

from firebase_admin import credentials, auth
from repository import Repository
from flask import request

# from app import get_auth

repository = Repository()


class Event(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo
        self.uid = request.headers.get("Authorization").split(' ')[1]

    def get(self, event_id=None, title=None, req=request):
        # if request.endpoint == 'get_#likes':
        #     print("getting number of likes")
        #     event = self.repo.get_likes(int(event_id))

        if event_id is not None:
            try:
                decoded_token = auth.verify_id_token(self.uid)
                print("User verified")
                event = self.repo.get_event_by_id(int(event_id), decoded_token['uid'])
                if event is None:
                    return {"idError": f"Event with the id {event_id} not found"}
                return event.__dict__
            except Exception as e:
                print('User unable to be verified or some other error has occured')
                print(e)

        if title is not None:
            try:
                decoded_token = auth.verify_id_token(self.uid)
                print("User verified")
                event = self.repo.get_event_by_title(title, current_user=decoded_token['uid'])
                if event is None:
                    return {"titleError": f"Event with the title {title} not found"}
                return event.__dict__
            except Exception as e:
                print('User unable to be verified or some other error has occured')
                print(e)

    def put(self, req=request):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("User verified")
            data = req.get_json()
            event = self.repo.update_event(data)
            return event.__dict__
        except Exception as e:
            print('User unable to be verified or some other error has occured')
            print(e)

    def delete(self, event_id):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("User verified")
            self.repo.delete_event(event_id, decoded_token['user_id'])
        except Exception as e:
            print('User unable to be verified or some other error has occurred')
            print(e)
            return 'User unable to be verified or some other error has occurred'

    def post(self, req=request):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("User verified")
            data = req.get_json()
            if request.endpoint == 'like_event':
                event = self.repo.like_event(data, decoded_token['uid'])
                return event.__dict__
        except Exception as e:
            print('User unable to be verified or some other error has occurred')
            print(e)
            return 'User unable to be verified or some other error has occurred'


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
            return [event.__dict__ for event in self.repo.get_all_events(decoded_token['uid'])]
        except Exception as e:
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


class Profile(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo
        self.uid = request.headers.get('Authorization').split(' ')[1]

    def get(self):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            if request.endpoint == 'created_by_user':
                return [event.__dict__ for event in self.repo.get_events_by_user(decoded_token['uid'])]
            elif request.endpoint == 'liked_by_user':
                return [event.__dict__ for event in self.repo.get_events_liked_by_user(decoded_token['uid'])]

        except Exception as e:
            print('User unable to be verified or some other error')
            print(e)
            return 'User unable to be verified'


class Comments(Resource):
    def __init__(self, repo=Repository()):
        self.repo = repo
        self.uid = request.headers.get('Authorization').split(' ')[1]

    def get(self, event_id):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            if request.endpoint == 'get_comment_by_event':
                return [comment.__dict__ for comment in self.repo.get_comments_by_event(event_id)]

        except Exception as e:
            print('User unable to be verified or some other error')
            print(e)
            return 'User unable to be verified'

    def post(self, req=request):
        try:
            decoded_token = auth.verify_id_token(self.uid)
            print("Posting a comment...")
            print("User ID: ", decoded_token['uid'])
            data = req.get_json()
            return self.repo.add_comment(data, decoded_token['uid']).__dict__

        except Exception as e:
            print('User unable to be verified or some other error.')
            print(e)
            return 'User unable to be verified'
