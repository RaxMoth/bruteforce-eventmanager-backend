from models import EventModel
from routes import *
from repository import Repository
from unittest.mock import MagicMock
from flask import Request
from app import app

event1 = EventModel(title='test Title 1', id=1, user_id='Admin', likes=0)
event2 = EventModel(title='test Title 2', id=2, user_id='Admin', likes=1)


def test_eventlist_get():
    repo = MagicMock(spec=Repository)
    repo.get_all_events.return_value = [event1, event2]
    events = EventList(repo).get()
    assert events[0]['id'] == 1
    assert events[1]['title'] == 'test Title 2'

def test_event_get():
    repo = MagicMock(spec=Repository)
    repo.get_event_by_id.return_value = event2
    event = Event(repo).get(2)
    assert event['id'] == 2
    assert event['title'] == 'test Title 2'


def test_eventlist_post():
    with app.test_request_context():
        repo = MagicMock(spec=Repository)
        req = MagicMock(spec=Request)
        data = EventModel(title='test Tile 3', user_id=301, likes=1)
        req.json.return_value = data.__dict__
        repo.add_event.return_value = EventModel(title='test Tile 3', id=3, user_id=301, likes=1)
        event = EventList(repo).post(req)
        assert event['id'] == 3
        assert event['title'] == 'test Tile 3'


