from flask_restful import Resource


class Event(Resource):
    def get(self, event_id=1):
        return {'Events': f'{event_id} works'}


class EventList(Resource):
    def get(self):
        return {'EventList': 'works'}

