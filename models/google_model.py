timezone = 'America/Argentina/Buenos_Aires'

class event_calendar:
    def __init__(self, summary, start_datetime, end_datetime, location=None, description=None, reminder_minutes=60):
        self.summary = summary
        self.location = location
        self.description = description
        self.start = {
            'dateTime': start_datetime,
            'timeZone': timezone
        }
        self.end = {
            'dateTime': end_datetime,
            'timeZone': timezone
        }
        self.reminders = {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': reminder_minutes},
            ]
        }

    def to_dict(self):
        event_dict = {
            'summary': self.summary,
            'location': self.location,
            'description': self.description,
            'start': self.start,
            'end': self.end,
            'reminders': self.reminders
        }       
        event_dict = {k: v for k, v in event_dict.items() if v is not None}

        return event_dict