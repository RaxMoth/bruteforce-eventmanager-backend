from models import EventModel, UserModel
import psycopg2
import os

# user1 = UserModel(1, 'Lalit')
# user2 = UserModel(2, 'Max')
# event1 = EventModel(1, 'Event 1')
# event2 = EventModel(2, 'Event 2')
# event3 = EventModel(3, 'Event 3')
# event4 = EventModel(4, 'Event 4')

host = os.environ['HOST']
database = os.environ['DATABASE']
db_port = os.environ['DB_PORT']
user = os.environ['USER']
password = os.environ['PASSWORD']


class Repository:
    def get_all_events(self):
        conn = None
        event_list = []
        try:
            conn = self.get_db()
            if conn:
                ps_cursor = conn.cursor()
                ps_cursor.execute("Select event_id, title, image, username from events")
                event_records = ps_cursor.fetchall()
                for row in event_records:
                    event_list.append(EventModel(id=row[0], title=row[1], likes=0, image=row[2], user_id=row[3]))
                ps_cursor.close()
            return event_list

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_event_by_id(self, event_id):
        conn = None
        try:
            conn = self.get_db()
            event = None
            if conn:
                ps_cursor = conn.cursor()
                ps_cursor.execute(f"Select event_id, title, image, username from events where event_id = %d;", (event_id))
                event_records = ps_cursor.fetchall()
                if len(event_records) < 1:
                    print("Event not found, check your id.")
                    ps_cursor.close()
                    return None
                for row in event_records:
                    event = EventModel(id=row[0], title=row[1], likes=0, image=row[2], user_id=row[3])
                ps_cursor.close()
            return event
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_event_by_title(self, title):
        conn = None
        try:
            conn = self.get_db()
            event = None
            if conn:
                ps_cursor = conn.cursor()
                title += '%'
                ps_cursor.execute(f"Select event_id, title, image, username from events where title similar to %s", (title))
                event_records = ps_cursor.fetchall()
                if len(event_records) < 1:
                    print("Event not found, check your title.")
                    ps_cursor.close()
                    return None
                for row in event_records:
                    event = EventModel(id=row[0], title=row[1], likes=0, image=row[2], user_id=row[3])
                ps_cursor.close()
            return event
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

    def add_event(self, data):
        conn = None
        try:
            conn = self.get_db()
            event = None
            if conn:
                ps_cursor = conn.cursor()
                if 'username' not in data: # remove this!
                    data['username'] ='Admin'
                if 'image' not in data:
                    data['image'] = ''
                # print(data)
                ps_cursor.execute(f"INSERT INTO events (title, username, image) VALUES (%s, %s, %s) RETURNING event_id", (data['title'], data['username'], data['image']))
                conn.commit()
                event_id = ps_cursor.fetchone()[0]
                if event_id is None:
                    ps_cursor.close()
                    print(event_id)
                    print("insertion unsuccessful")
                    return None
                ps_cursor.close()
                event = EventModel(id=event_id, title=data['title'], likes=0, image=data['image'], user_id=data['username'])
            return event

        except Exception as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

# if __name__ == '__main__':
