from models import EventModel, UserModel
import psycopg2
from flask import current_app, g

# user1 = UserModel(1, 'Lalit')
# user2 = UserModel(2, 'Max')
# event1 = EventModel(1, 'Event 1')
# event2 = EventModel(2, 'Event 2')
# event3 = EventModel(3, 'Event 3')
# event4 = EventModel(4, 'Event 4')

# host = os.environ['HOST']
# database = os.environ['DATABASE']
# db_port = os.environ['DB_PORT']
# user = os.environ['USER']
# password = os.environ['PASSWORD']


class Repository:
    def get_all_events(self):
        event_list = []
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute("Select event_id, title, image, username, loc, eventdate, description from events")
            event_records = ps_cursor.fetchall()
            for row in event_records:
                event_list.append(EventModel(id=row[0], title=row[1], likes=0, image=row[2], user_id=row[3], location=row[4], date=str(row[5]), description=row[6]))
            ps_cursor.close()
        return event_list


    def get_event_by_id(self, event_id):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(f"Select event_id, title, image, username, description, eventdate, loc from events where event_id = %s;", [event_id])
            event_records = ps_cursor.fetchall()
            if len(event_records) < 1:
                print("Event not found, check your id.")
                ps_cursor.close()
                return None
            for row in event_records:
                event = EventModel(id=row[0], title=row[1], likes=0, image=row[2], user_id=row[3], description= row[4], date=str(row[5]), location=row[6])
            ps_cursor.close()
        return event

    def get_event_by_title(self, title):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            title += '%'
            ps_cursor.execute(f"Select event_id, title, image, username, description, eventdate, loc from events where title similar to %s", (title))
            event_records = ps_cursor.fetchall()
            if len(event_records) < 1:
                print("Event not found, check your title.")
                ps_cursor.close()
                return None
            for row in event_records:
                event = EventModel(id=row[0], title=row[1], likes=0, image=row[2], user_id=row[3], description= row[4], date=str(row[5]), location=row[6])
            ps_cursor.close()
        return event


    def get_db(self):
        if 'db' not in g:
            g.db = current_app.config['pSQL_pool'].getconn()
        return g.db

    def add_event(self, data):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            if 'username' not in data: # remove this!
                data['username'] ='Admin'
            if 'image' not in data:
                data['image'] = ''
            ps_cursor.execute(f"INSERT INTO events (title, description, username, image, loc, eventdate) VALUES (%s, %s, %s, %s, %s, %s) RETURNING event_id", (data['title'], data['description'], data['username'], data['image'], data['location'], data['date']))
            conn.commit()
            event_id = ps_cursor.fetchone()[0]
            if event_id is None:
                ps_cursor.close()
                print(event_id)
                print("insertion unsuccessful")
                return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=0, image=data['image'], user_id=data['username'], description=data["description"], location=data["location"], date=data["date"])
        return event

    def update_event(self, data):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(f"UPDATE events SET title = %s,  description = %s, loc= %s, eventdate = %s WHERE event_id= %s  RETURNING event_id", (data['title'], data['description'], data['location'], data['date'], data['id']))
            conn.commit()
            event_id = ps_cursor.fetchone()[0]
            if event_id is None:
                ps_cursor.close()
                print(event_id)
                print("Update unsuccessful")
                return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=data['likes'], image=data['image'], user_id=data['id'], location=data['location'], description=data['description'], date=data['date'])
        return event
    
    def delete_event(self, event_id):
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            print(event_id, str(event_id))
            ps_cursor.execute(f"DELETE FROM events WHERE event_id= %s;",  [event_id])
            conn.commit()
            ps_cursor.close()
        




# if __name__ == '__main__':
