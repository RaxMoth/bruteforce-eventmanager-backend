from flask import Flask
from flask_restful import Api
from routes import Event, EventList
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)
BASE_URL = '/api'

api.add_resource(Event, f'{BASE_URL}/event/')
api.add_resource(EventList, f'{BASE_URL}/events')


if __name__ == '__main__':
    app.run(debug=True)

