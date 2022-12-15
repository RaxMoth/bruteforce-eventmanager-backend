import base64
import uuid

from models import EventModel, UserModel, CommentModel
import psycopg2
from flask import current_app, g, jsonify
from datetime import datetime
from google.cloud import storage


class Repository:
    def get_all_events(self, current_user):
        event_list = []
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(
                "Select event_id, title, image, username, loc, eventdate, description, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events")
            event_records = ps_cursor.fetchall()
            for row in event_records:
                ps_cursor.execute(f"select * from events_liked where username=%s and event_id=%s",
                                  (current_user, row[0]))
                isLiked = False
                if len(ps_cursor.fetchall()) > 0:
                    isLiked = True
                event_list.append(
                    EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], location=row[4], date=str(row[5]),
                               description=row[6], likes=row[7], isLiked=isLiked))
            ps_cursor.close()
        return event_list

    def get_event_by_id(self, event_id, current_user):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(
                f"Select event_id, title, image, username, description, eventdate, loc, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events where event_id = %s;",
                [event_id])
            event_records = ps_cursor.fetchall()
            if len(event_records) < 1:
                print("Event not found, check your id.")
                ps_cursor.close()
                return None
            for row in event_records:
                ps_cursor.execute(f"select * from events_liked where username=%s and event_id=%s",
                                  (current_user, row[0]))
                isLiked = False
                if len(ps_cursor.fetchall()) > 0:
                    isLiked = True
                event = EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], description=row[4],
                                   date=str(row[5]), location=row[6], likes=row[7], isLiked=isLiked)
            ps_cursor.close()
        return event

    def get_event_by_title(self, title, current_user):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            title += '%'
            ps_cursor.execute(
                f"Select event_id, title, image, username, description, eventdate, loc, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events where title similar to %s",
                (title,))
            event_records = ps_cursor.fetchall()
            if len(event_records) < 1:
                print("Event not found, check your title.")
                ps_cursor.close()
                return None
            for row in event_records:
                ps_cursor.execute(f"select * from events_liked where username=%s and event_id=%s",
                                  (current_user, row[0]))
                isLiked = False
                if len(ps_cursor.fetchall()) > 0:
                    isLiked = True
                event = EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], description=row[4],
                                   date=str(row[5]), location=row[6], likes=row[7], isLiked=isLiked)
            ps_cursor.close()
        return event

    def get_events_by_user(self, current_user):
        event_list = []
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(
                "Select event_id, title, image, username, loc, eventdate, description, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events where username=%s",
                (current_user,))
            event_records = ps_cursor.fetchall()
            for row in event_records:
                ps_cursor.execute(f"select * from events_liked where username=%s and event_id=%s",
                                  (current_user, row[0]))
                isLiked = False
                if len(ps_cursor.fetchall()) > 0:
                    isLiked = True
                event_list.append(
                    EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], location=row[4], date=str(row[5]),
                               description=row[6], likes=row[7], isLiked=isLiked))
            ps_cursor.close()
        return event_list

    def get_events_liked_by_user(self, current_user):
        event_list = []
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(
                "Select event_id, title, image, username, loc, eventdate, description, (SELECT COUNT(*) FROM events_liked WHERE events_liked.event_id = events.event_id) AS likes from events where event_id in (select event_id from events_liked where username=%s)",
                (current_user,))
            event_records = ps_cursor.fetchall()
            for row in event_records:
                ps_cursor.execute(f"select * from events_liked where username=%s and event_id=%s",
                                  (current_user, row[0]))
                isLiked = False
                if len(ps_cursor.fetchall()) > 0:
                    isLiked = True
                event_list.append(
                    EventModel(id=row[0], title=row[1], image=row[2], user_id=row[3], location=row[4], date=str(row[5]),
                               description=row[6], likes=row[7], isLiked=isLiked))
            ps_cursor.close()
        return event_list

    def get_comments_by_event(self, event_id):
        comments = []
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(
                f"Select comment_id, event_id, u_comment, comment_date, username, first_name, last_name from comments where event_id=%s",
                [event_id])
            comments_sql = ps_cursor.fetchall()
            for row in comments_sql:
                # print("username", row[4])
                # print("comment", row[2])
                comments.append(CommentModel(comment_id=row[0], event_id=row[1], u_comment=row[2], comment_date=str(row[3]),
                                             username=row[4], first_name=row[5], last_name=row[6]))
            ps_cursor.close()
        return comments

    def get_db(self):
        if 'db' not in g:
            g.db = current_app.config['pSQL_pool'].getconn()
        return g.db

    def add_comment(self, data, current_user):
        conn = self.get_db()
        data['username'] = current_user
        # print(current_user)
        comment = None
        if conn:
            ps_cursor = conn.cursor()

            user = self.get_user_by_id(current_user)
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name

            if 'comment_date' not in data:
                data['comment_date'] = str(datetime.now())
            try:
                ps_cursor.execute(
                    f"INSERT INTO COMMENTS (u_comment, event_id, username, comment_date, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s) RETURNING comment_id",
                    (data['u_comment'], data['event_id'], data['username'], data['comment_date'], data['first_name'], data['last_name']))
                conn.commit()

                print("Comment posted successfully")
            except Exception as e:
                print("Comment posting failed")
                print(e)
            comment_id = ps_cursor.fetchone()[0]
            ps_cursor.close()
            comment = CommentModel(comment_id=comment_id, u_comment=data['u_comment'], event_id=data['event_id'], username=data['username'], comment_date=data['comment_date'], first_name=data['first_name'], last_name=data['last_name'])
        return comment

    def add_event(self, data, username):
        conn = self.get_db()
        event = None
        data['username'] = username
        if conn:
            ps_cursor = conn.cursor()
            if 'username' not in data:  # remove this!
                data['username'] = username
            if 'image' not in data or len(data['image']) < 1:
                data['image'] = ''
            else:
                print("Trying to create new image...")
                image = data['image']
                # print(len(image))
                storage_client = storage.Client()
                # print(storage_client.list_buckets())
                bucket = storage_client.bucket("event_images_roi_training")
                # print(bucket)
                blob_name = "event/image_" + username + "_" + str(uuid.uuid4())
                # print(blob_name)
                blob = bucket.blob(blob_name)
                # print("1")
                img_type, image = image.split(',')
                # print("img type =" , img_type)
                decoded_image = base64.b64decode(image)
                img_format = img_type.split('/')[1].split(';')[0]
                # print(img_format, len(decoded_image))
                blob.upload_from_string(decoded_image, content_type=img_format)
                blob.make_public()
                print("Image uploaded to google storage successfully. Public media link is: ", blob.media_link)
                data['image'] = "https://storage.googleapis.com/event_images_roi_training/" + blob_name

            try:
                ps_cursor.execute(
                    f"INSERT INTO events (title, description, username, image, loc, eventdate) VALUES (%s, %s, %s, %s, %s, %s) RETURNING event_id",
                    (data['title'], data['description'], data['username'], data['image'], data['location'],
                     data['date']))
                conn.commit()
            except Exception as e:
                print("Error: ", e)
            event_id = ps_cursor.fetchone()[0]
            if event_id is None:
                ps_cursor.close()
                # print(event_id)
                print("Event insertion unsuccessful, Event id: ", str(event_id))
                return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=0, image=data['image'], user_id=data['username'],
                               description=data["description"], location=data["location"], date=data["date"])
        return event

    def get_user_by_id(self, username):
        conn = self.get_db()
        user = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(f"Select username, dark_mode, u_email, u_fname, u_lname from users where username = %s;",
                              (username,))
            user_records = ps_cursor.fetchall()
            if len(user_records) < 1:
                print("User not found, check your username.")
                ps_cursor.close()
                return None
            for row in user_records:
                user = UserModel(user_id=row[0], dark_mode=row[1], user_email=row[2], first_name=row[3],
                                 last_name=row[4])
            ps_cursor.close()
            # print(user.first_name, user.last_name, user.user_email)
        return user

    def update_event(self, data):
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            ps_cursor.execute(
                f"UPDATE events SET title = %s,  description = %s, loc= %s, eventdate = %s WHERE event_id= %s  RETURNING event_id",
                (data['title'], data['description'], data['location'], data['date'], data['id']))
            conn.commit()
            event_id = ps_cursor.fetchone()[0]
            if event_id is None:
                ps_cursor.close()
                # print(event_id)
                print("Update unsuccessful")
                return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=data['likes'], image=data['image'],
                               user_id=data['id'], location=data['location'], description=data['description'],
                               date=data['date'])
        return event

    def like_event(self, data, user_id='Admin'):
        # print("liking event")
        conn = self.get_db()
        event = None
        if conn:
            ps_cursor = conn.cursor()
            if 'current_user' not in data:
                data['current_user'] = user_id
            data['liked_time'] = datetime.now()
            # print(data)

            ps_cursor.execute(f"SELECT * FROM events_liked where username=%s and event_id=%s",
                              (data['current_user'], data["id"]))
            conn.commit()
            if len(ps_cursor.fetchall()) > 0:
                ps_cursor.execute(f"DELETE FROM events_liked where username=%s and event_id=%s returning event_id",
                                  (data['current_user'], data['id']))
                conn.commit()
                event_id = ps_cursor.fetchone()[0]
            else:
                ps_cursor.execute(
                    f"INSERT into events_liked (username, event_id, liked_time) VALUES (%s, %s, %s) RETURNING event_id",
                    (data["current_user"], data["id"], data["liked_time"]))
                conn.commit()
                id, _, event_id = ps_cursor.fetchone()[:3]
                if id is None:
                    ps_cursor.close()
                    # print(id)
                    print("Like unsuccessful")
                    return None
            ps_cursor.close()
            event = EventModel(id=event_id, title=data['title'], likes=data['likes'], image=data['image'],
                               user_id=data['id'], location=data['location'], description=data['description'],
                               date=data['date'])
        return event

    def delete_event(self, event_id, user_id):
        conn = self.get_db()
        if conn:
            ps_cursor = conn.cursor()
            # print(event_id, str(event_id))
            ps_cursor.execute(f"DELETE FROM events WHERE event_id= %s AND username = %s;", [event_id, user_id])
            conn.commit()
            ps_cursor.close()

    def add_user(self, data):
        user  = self.get_user_by_id(data['username'])
        if (user is not None):
            print("user already exists")
            return self.get_user_by_id(data['username'])
        conn = self.get_db()
        user = None
        if conn:
            ps_cursor = conn.cursor()
            # print(data)
            ps_cursor.execute(
                f"INSERT INTO users (username, dark_mode, u_email, u_lname, u_fname) VALUES (%s, %s, %s, %s, %s) RETURNING username",
                (data['username'], data['dark_mode'], data['email'], data['last_name'], data['first_name']))
            conn.commit()
            username = ps_cursor.fetchone()[0]
            if username is None:
                ps_cursor.close()
                # print(username)
                print("insertion unsuccessful")
                return None
            ps_cursor.close()
            user = UserModel(user_id=username, user_email=data['email'], dark_mode=data['dark_mode'],
                             first_name=data['first_name'], last_name=data['last_name'])
        return user

# if __name__ == '__main__':
