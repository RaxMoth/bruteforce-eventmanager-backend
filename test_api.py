import routes
from models import EventModel
from unittest.mock import patch
from unittest import TestCase
import unittest
from app import app
import json


BASE_URL = '/api'
# event1 = EventModel(title='test Title 1', id=1, user_id=101, likes=0)
# event2 = EventModel(title='test Title 2', id=2, user_id=201, likes=1)

class ApiTests(TestCase):

    @patch('routes.EventList.get')
    def test_events(self, test_patch):
        with app.test_client() as client:
            # test_patch.return_value = [event1.__dict__, event2.__dict__]
            response = client.get(f'{BASE_URL}/Events')
            assert response.status_code == 200
            events = json.loads(response.data)
            assert events[0]['id'] == 1

    @patch('routes.Event.get')
    def test_event_by_id(self, test_patch):
        with app.test_client() as client:
            # test_patch.return_value = [event1.__dict__, event2.__dict__]
            response = client.get(f'{BASE_URL}/Events/1')
            assert response.status_code == 200
            events = json.loads(response.data)
            assert events[0]['id'] == 1