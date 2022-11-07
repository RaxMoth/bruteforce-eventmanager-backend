from flask import Flask
from flask_restful import Resource, Api
from routes import Event, EventList


app = Flask(__name__)
api = Api(app)
BASE_URL = '/api'

api.add_resource(Event, f'{BASE_URL}/Events/<event_id>')
api.add_resource(EventList, f'{BASE_URL}/Events')


if __name__ == '__main__':
    app.run(debug=True, port=32413)

