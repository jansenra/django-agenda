from datetime import datetime, timedelta
from django.db.models.manager import Manager

class EventManager(Manager):

    def get_upcomming(self):
        now = datetime.now()
        return self.get_query_set().filter(start_date__gte=now - timedelta(days=1))

    def get_by_date(self, year=None, month=None, day=None):
        events = self.get_query_set()

        if not year:
            return events

        events = events.filter(start_date__year=year)

        if not month:
            return events

        events = events.filter(start_date__month=month)

        if not day:
            return events

        return events.filter(start_date__day=day)
