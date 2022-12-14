from flask import Flask, g, request
from flask_restful import Api
from routes import Event, EventList, User, Profile, Comments
from flask_cors import CORS
import os
from psycopg2 import pool

import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate(os.environ.get('FIREBASE_CRED'))
auth_app = firebase_admin.initialize_app(cred)


app = Flask(__name__)
CORS(app)
api = Api(app)
BASE_URL = os.environ.get('BASE_URL', default='/api')

host = os.environ.get('HOST', default='localhost')
database = os.environ.get('DATABASE', default='events')
db_port = os.environ.get('DB_PORT', default=5432)
user = os.environ.get('USER', default='postgres')
password = os.environ.get('PASSWORD', default='postgres')
MIN = os.environ.get('MIN', default=1)
MAX = os.environ.get('MAX', default=5)
DEBUG = os.environ.get('DEBUG', default=True)
PORT = os.environ.get('PORT', default=5000)
# print(host, database, )
app.config['pSQL_pool'] = pool.SimpleConnectionPool(MIN, MAX, host=host, database=database, port=db_port, user=user, password=password)


api.add_resource(EventList, f'{BASE_URL}/events')
api.add_resource(Event, f'{BASE_URL}/event/<event_id>', f'{BASE_URL}/eventbytitle/<title>')

api.add_resource(Event, f'{BASE_URL}/event', endpoint ='update_event')
# api.add_resource(Event, f'{BASE_URL}/event/likes/<event_id>', endpoint ='get_#likes')
api.add_resource(Event, f'{BASE_URL}/event/like', endpoint ='like_event')
api.add_resource(User, f'{BASE_URL}/user', f'{BASE_URL}/user/<username>')


api.add_resource(Profile, f'{BASE_URL}/profile/created_events', endpoint="created_by_user")
api.add_resource(Profile, f'{BASE_URL}/profile/liked_events', endpoint="liked_by_user")
api.add_resource(Comments, f'{BASE_URL}/comments/<event_id>', f'{BASE_URL}/comments')

# api.add_resource(Event, f'{BASE_URL}/event_by_user/<user_id>')
# perform cd

@app.teardown_appcontext
def close_conn(e):
    db = g.pop('db', None)
    if db is not None:
        app.config['pSQL_pool'].putconn(db)
        print('released connection back to pool')
        # print('redeployment works!')

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)

