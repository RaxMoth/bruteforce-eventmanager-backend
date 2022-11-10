import routes
from models import EventModel
from unittest.mock import patch
from unittest import TestCase
import unittest
from app import app
import json


BASE_URL = '/api'
event1 = EventModel(title='test Title 1', user_id='Admin', likes=0, image='')
event2 = EventModel(title='test Title 2', user_id='Admin', likes=1, image='')

class ApiTests(TestCase):

    @patch('routes.EventList.get')
    def test_events(self, test_patch):
        with app.test_client() as client:
            test_patch.return_value = [event1.__dict__, event2.__dict__]
            response = client.get(f'{BASE_URL}/Events')
            assert response.status_code == 200
            events = json.loads(response.data)
            assert events[1]['inasd'] == 4

    @patch('routes.Event.get')
    def test_events(self, test_patch):
        with app.test_client() as client:
            # test_patch.return_value = [event1.__dict__, event2.__dict__]
            response = client.get(f'{BASE_URL}/Events')
            assert response.status_code == 200
            events = json.loads(response.data)
            assert events[0]['id'] == 1