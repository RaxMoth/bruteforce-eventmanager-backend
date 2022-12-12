import base64
import uuid

from models import EventModel, UserModel
import psycopg2
from flask import current_app, g, jsonify
from datetime import datetime
from google.cloud import storage



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
            ps_cursor.execute("Select event_id, title, image, username, loc, eventdate, description, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events")
            event_records = ps_cursor.fetchall()
            for row in event_records:
                event_list.append(EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], location=row[4], date=str(row[5]), description=row[6], likes=row[7]))
            ps_cursor.close()
        return event_list


    def get_event_by_id(self, event_id):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(f"Select event_id, title, image, username, description, eventdate, loc, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events where event_id = %s;", [event_id])
            event_records = ps_cursor.fetchall()
            if len(event_records) < 1:
                print("Event not found, check your id.")
                ps_cursor.close()
                return None
            for row in event_records:
                event = EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], description= row[4], date=str(row[5]), location=row[6], likes=row[7])
            ps_cursor.close()
        return event

    def get_event_by_title(self, title):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            title += '%'
            ps_cursor.execute(f"Select event_id, title, image, username, description, eventdate, loc, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events where title similar to %s", (title,))
            event_records = ps_cursor.fetchall()
            if len(event_records) < 1:
                print("Event not found, check your title.")
                ps_cursor.close()
                return None
            for row in event_records:
                event = EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], description= row[4], date=str(row[5]), location=row[6], likes = row[7])
            ps_cursor.close()
        return event


    def get_db(self):
        if 'db' not in g:
            g.db = current_app.config['pSQL_pool'].getconn()
        return g.db

    def add_event(self, data, username):
        conn = self.get_db()
        event = None
        data['username'] = username
        if conn:
            ps_cursor = conn.cursor()
            if 'username' not in data: # remove this!
                data['username'] = username
            if 'image' not in data:
                data['image'] = ''
            else:
                print("Trying to create new image...")
                image = data['image']
                storage_client = storage.Client()
                print(storage_client.list_buckets())
                bucket = storage_client.bucket("event_images_roi_training")
                # print(bucket)
                blob_name = "event/image_"+username+"_"+str(uuid.uuid4())
                print(blob_name)
                blob = bucket.blob(blob_name)
                img_type, image = image.split(',')
                decoded_image = base64.b64decode(image)
                img_format = img_type.split('/')[1].split(';')[0]
                print(img_format, len(decoded_image))
                blob.upload_from_string(decoded_image, content_type=img_format)
                blob.make_public()
                print("Image uploaded to google storage successfully. Public media link is: ", blob.media_link)
                data['image'] = "https://storage.googleapis.com/event_images_roi_training/"+blob_name

            try:
                ps_cursor.execute(f"INSERT INTO events (title, description, username, image, loc, eventdate) VALUES (%s, %s, %s, %s, %s, %s) RETURNING event_id", (data['title'], data['description'], data['username'], data['image'], data['location'], data['date']))
                conn.commit()
            except Exception as e:
                print("Error: ", e)
            event_id = ps_cursor.fetchone()[0]
            if event_id is None:
                ps_cursor.close()
                print(event_id)
                print("insertion unsuccessful")
                return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=0, image=data['image'], user_id=data['username'], description=data["description"], location=data["location"], date=data["date"])
        return event


    def get_user_by_id(self, username):
        conn = self.get_db()
        user = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(f"Select username, pass, u_email, u_fname, u_lname from users where username = %s;", (username,))
            user_records = ps_cursor.fetchall()
            if len(user_records) < 1:
                print("User not found, check your username.")
                ps_cursor.close()
                return None
            for row in user_records:
                user = UserModel(user_id=row[0], password=row[1], user_email=row[2], first_name=row[3], last_name=row[4])
            ps_cursor.close()
        return user

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

    def like_event(self, data):
        print("liking event")
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            if 'user_id' not in data:
                data['user_id'] = 'Admin'
            data['liked_time'] = datetime.now()
            print(data)
            ps_cursor.execute(f"INSERT into events_liked (username, event_id, liked_time) VALUES (%s, %s, %s) RETURNING id",(data["user_id"], data["id"], data["liked_time"]))
            conn.commit()
            event_id = ps_cursor.fetchone()[0]
            if id is None:
                ps_cursor.close()
                print(id)
                print("Like unsuccessful")
                return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=data['likes'], image=data['image'], user_id=data['id'], location=data['location'], description=data['description'], date=data['date'])
        return event
    
    
    def delete_event(self, event_id, user_id):
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            print(event_id, str(event_id))
            ps_cursor.execute(f"DELETE FROM events WHERE event_id= %s AND username = %s;",  [event_id, user_id])
            conn.commit()
            ps_cursor.close()


    def add_user(self, data):
        conn = self.get_db()
        user = None
        if conn:
            ps_cursor = conn.cursor()
            if 'u_fname' not in data:  # remove this!
                data['u_fname'] = 'Admin'
            if 'u_lname' not in data:
                data['u_lname'] = ''

            # print(data)
            ps_cursor.execute(f"INSERT INTO users (username, password, u_email, u_lname, u_fname) VALUES (%s, %s, %s, %s, %s) RETURNING username",
                              (data['username'], data['password'], data['u_email'], data['u_lname'], data['u_fname']))
            conn.commit()
            username = ps_cursor.fetchone()[0]
            if username is None:
                ps_cursor.close()
                print(username)
                print("insertion unsuccessful")
                return None
            ps_cursor.close()
            user = UserModel(user_id=username, user_email=data['u_email'], password=data['password'], first_name=data['u_fname'], last_name=data['u_lname'])
        return user
# if __name__ == '__main__':
