from models import EventModel
from flask import Flask
import psycopg2
from psycopg2 import pool
from repository import Repository
from unittest.mock import MagicMock

event1 = EventModel(title='test Title 1', user_id='Admin', likes=0, image='')
event2 = EventModel(title='test Title 2', user_id='Admin', likes=1, image='')

eventrow = [(1, event1.title, event1.image, event1.user_id), (2, event2.title, event2.image, event2.user_id)]

def test_events_get_all():
    app = Flask(__name__)
    with app.app_context():
        p_mock = MagicMock(spec=psycopg2.pool.SimpleConnectionPool)
        app.config['pSQL_pool'] = p_mock
        conn_mock = MagicMock(spec=psycopg2.extensions.connection)
        cursor_mock = MagicMock()
        p_mock.getconn.return_value = conn_mock
        conn_mock.cursor.return_value = cursor_mock
        cursor_mock.fetchall.return_value = eventrow

        repo = Repository()
        events = repo.get_all_events()
        assert events[0].title == event1.title
        assert events[1].user_id == event2.user_id


def test_get_event_by_id():
    app = Flask(__name__)
    with app.app_context():
        p_mock = MagicMock(spec=psycopg2.pool.SimpleConnectionPool)
        app.config['pSQL_pool'] = p_mock
        conn_mock = MagicMock(spec=psycopg2.extensions.connection)

        cursor_mock = MagicMock()
        p_mock.getconn.return_value = conn_mock
        conn_mock.cursor.return_value = cursor_mock
        cursor_mock.fetchall.return_value = [eventrow[0]]

        repo = Repository()
        events = repo.get_event_by_id(1)

        assert events.title == event1.title


def test_get_event_by_title():
    app = Flask(__name__)
    with app.app_context():
        p_mock = MagicMock(spec=psycopg2.pool.SimpleConnectionPool)
        app.config['pSQL_pool'] = p_mock
        conn_mock = MagicMock(spec=psycopg2.extensions.connection)

        cursor_mock = MagicMock()
        p_mock.getconn.return_value = conn_mock
        conn_mock.cursor.return_value = cursor_mock
        cursor_mock.fetchall.return_value = [eventrow[0]]

        repo = Repository()
        events = repo.get_event_by_title('test Title 1')

        assert events.user_id == event1.user_id


