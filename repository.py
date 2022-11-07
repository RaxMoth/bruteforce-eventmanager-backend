from models import EventModel, UserModel


user1 = UserModel(1, 'Lalit')
user2 = UserModel(2, 'Max')

event1 = EventModel(1, 'Event 1')
event2 = EventModel(2, 'Event 2')
event3 = EventModel(3, 'Event 3')
event4 = EventModel(4, 'Event 4')
events = [event1, event2, event3, event4]

class Repository:
    def events_get_all(self):
        return events

    def event_get_by_id(self, id):
        return next((x for x in events if x.id == id), None)

    def event_add(self, data):
        print(list(data.values()))
        new_event = EventModel(*list(data.values()))
        events.append(new_event)
        return new_event

# if __name__ == '__main__':
