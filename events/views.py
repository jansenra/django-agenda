import datetime
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404

from .models import Event, EventUsers
from .forms import RsvpForm
from .html_calendar import EventCalendar

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
        context['attendees'] = EventUsers.objects.filter(event=self.object, rsvp="going")
        user_rsvp = ""
        try:
            rsvp = EventUsers.objects.get(event=self.object, user=self.request.user)
            user_rsvp = rsvp.rsvp
        except EventUsers.DoesNotExist:
            pass

        context['user_rsvp'] = user_rsvp

        return context


class ArchiveMixin(object):
    template_name = "events/archive.html"
    model = Event
    context_object_name = "events"


class Index(ArchiveMixin, ListView):
    template_name = "events/index.html"

    def get_queryset(self):
        return Event.objects.get_upcomming()

    def get_calendar(self, date_in):
        events = Event.objects.get_by_date(year=date_in.year, month=date_in.month)
        return EventCalendar(events).formatmonth(date_in.year, date_in.month)

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        this_month = datetime.date(today.year, today.month, 1)

        try:
            next_month = this_month.replace(month=this_month.month+1)
        except ValueError:
            next_month = this_month.replace(year=this_month.year+1, month=1)

        context = super(Index, self).get_context_data(**kwargs)
        context['calendar_this_month'] = self.get_calendar(this_month)
        context['calendar_next_month'] = self.get_calendar(next_month)

        return context

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


class RsvpCreate(CreateView):
    model = EventUsers
    _event = None
    template_name = "attendees/create.html"
    form_class = RsvpForm

    @property
    def event(self):
        if not self._event:
            self._event = get_object_or_404(Event, pk=self.request.POST.get('event_id'))
        return self._event

    def form_valid(self, form):
        rsvp = self.request.POST.get('rsvp')
        if rsvp == 'remove':
            try:
                object = EventUsers.objects.get(event=self.event, user=self.request.user)
                object.delete()
            except EventUsers.DoesNotExist:
                pass
            return HttpResponseRedirect(self.get_success_url())

        # check if a record already exists
        try:
            object = EventUsers.objects.get(event=self.event, user=self.request.user)
            object.rsvp = rsvp
            object.save()
            return HttpResponseRedirect(self.get_success_url())
        except EventUsers.DoesNotExist:
            pass

        object = form.save(commit=False)
        object.event = self.event
        object.user = self.request.user
        object.save()
        return super(RsvpCreate, self).form_valid(form)

    def get_success_url(self):
        return self.event.get_absolute_url()
