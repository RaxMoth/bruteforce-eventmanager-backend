from models import EventModel, UserModel
import psycopg2

user1 = UserModel(1, 'Lalit')
user2 = UserModel(2, 'Max')

event1 = EventModel(1, 'Event 1')
event2 = EventModel(2, 'Event 2')
event3 = EventModel(3, 'Event 3')
event4 = EventModel(4, 'Event 4')

host = '127.0.0.1'
database = 'events'
db_port = 5432
user = 'donadiv'
password = 'donadi12'


class Repository:
    def events_get_all(self):
        conn = None
        event_list = []
        try:
            conn = self.get_db()
            if conn:
                ps_cursor = conn.cursor()
                ps_cursor.execute("Select eventid, title, likes, image, userid from event")
                event_records = ps_cursor.fetchall()
                for row in event_records:
                    event_list.append(EventModel(id=row[0], title=row[1], likes=row[2], image=row[3], user_id=row[4]))
                ps_cursor.close()
            return event_list

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    def get_db(self):
        return psycopg2.connect(
            host=host,
            database=database,
            port=db_port,
            user=user,
            password=password)

# if __name__ == '__main__':
