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
    def __init__(self, user_id, user_email, password='root', first_name='', last_name=''):

        self.user_id = user_id
        self.user_email = user_email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name



class CommentModel:
    def __init__(self):
        pass


