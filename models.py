class EventModel:
    def __init__(self, title, id=1, description='', date=None, location='', user_id=-1, likes=0, image='', isLiked=False):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.user_id = user_id
        self.likes = likes
        self.image = image
        self.isLiked = isLiked


class UserModel:
    def __init__(self, user_id, user_email, dark_mode=False, first_name='', last_name=''):

        self.user_id = user_id
        self.user_email = user_email
        self.dark_mode = dark_mode
        self.first_name = first_name
        self.last_name = last_name




class CommentModel:
    def __init__(self, comment_id, u_comment, event_id, username, first_name, last_name="", comment_date=None):
        self.comment_id = comment_id
        self.u_comment = u_comment
        self.event_id = event_id
        self.username = username
        self.comment_date = comment_date
        self.first_name = first_name
        self.last_name = last_name

