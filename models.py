class EventModel:
    def __init__(self, id, title, description='', date=None, location='', user_id=-1, likes=0, image=''):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.user_id = user_id
        self.likes = likes
        self.image = image


class UserModel:
    def __init__(self, id, name, password='', dob=None):
        self.id = id
        self.name = name
        self.password = password
        self.dob = dob

