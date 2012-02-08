import datetime
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Event, EventCalendar

from apps.replies.views import ReplyMixin


class Detail(DetailView, ReplyMixin):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.get_by_date(year=self.kwargs['year'], month=self.kwargs['month'], day=self.kwargs['day'])\
            .filter(slug__contains=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['form'] = self.get_form(self.get_form_class())
        return context


class ArchiveMixin(object):
    template_name = "events/archive.html"
    model = Event
    context_object_name = "events"


class Index(ArchiveMixin, ListView):
    template_name = "events/index.html"

    def get_queryset(self):
        return Event.objects.get_upcomming()


class Day(ArchiveMixin, ListView):
    def get_queryset(self):
        return Event.objects.get_by_date(year=self.kwargs['year'], month=self.kwargs['month'], day=self.kwargs['day'])


class Month(ArchiveMixin, ListView):
    def get_queryset(self):
        return Event.objects.get_by_date(year=self.kwargs['year'], month=self.kwargs['month'])


class Year(ArchiveMixin, ListView):
    def get_queryset(self):
        return Event.objects.get_by_date(year=self.kwargs['year'])


class Calendar(ListView):
    """
    Gets called from AJAX, displays simple list of events on selected date
    """
    template_name = "events/calendar_list.html"
    model = Event
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.get_by_date(year=self.kwargs['year'], month=self.kwargs['month'], day=self.kwargs['day'])


class Widget(TemplateView):
    """
    Example of widget usage
    """
    def get_context_data(self, **kwargs):
        context = super(Widget, self).get_context_data(**kwargs)

        today = datetime.date.today()
        events = Event.objects.get_by_date(year=today.year, month=today.month)
        context['calendar'] = EventCalendar(events).formatmonth(today.year, today.month)

        return context
