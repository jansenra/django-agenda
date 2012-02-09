import calendar
from datetime import date
from itertools import groupby
from django.core.urlresolvers import reverse

class EventCalendar(calendar.HTMLCalendar):
    """
    Event calendar is a basic calendar made with HTMLCalendar module.
    """
    def __init__(self, events, *args, **kwargs):
        self.events = self.group_by_day(events)
        super(EventCalendar, self).__init__(*args, **kwargs)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                url = reverse('events-calendar', kwargs={'year': self.year, 'month': self.month, 'day': day})
                return self.day_cell(cssclass, '<a href="%s" class="view_events">%d</a>' % (url, day))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.start_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
