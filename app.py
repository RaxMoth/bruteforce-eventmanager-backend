from flask import Flask, g
from flask_restful import Api
from routes import Event, EventList
from flask_cors import CORS
import os
from psycopg2 import pool


app = Flask(__name__)
CORS(app)
api = Api(app)
BASE_URL = '/api'

host = os.environ.get('HOST', default='localhost')
database = os.environ.get('DATABASE', default='events')
db_port = os.environ.get('DB_PORT', default=5432)
user = os.environ.get('USER', default='postgres')
password = os.environ.get('PASSWORD', default='postgres')
MIN = os.environ.get('MIN', default=1)
MAX = os.environ.get('MAX', default=5)

app.config['pSQL_pool'] = pool.SimpleConnectionPool(MIN, MAX, host=host, database=database, port=db_port, user=user, password=password)
api.add_resource(EventList, f'{BASE_URL}/events')
api.add_resource(Event, f'{BASE_URL}/event', f'{BASE_URL}/event/<event_id>', f'{BASE_URL}/eventbytitle/<title>')




@app.teardown_appcontext
def close_conn(e):
    db = g.pop('db', None)
    if db is not None:
        app.config['pSQL_pool'].putconn(db)
        print('released connection back to pool')

if __name__ == '__main__':
    app.run(debug=True)