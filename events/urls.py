from django.conf.urls.defaults import patterns, url

from .views import Detail, Year, Month, Day, Index, Calendar

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        Detail.as_view(), name='events-detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        Day.as_view(), name='events-archive-day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        Month.as_view(), name='events-archive-month'),

    url(r'^(?P<year>\d{4})/$',
        Year.as_view(), name='events-archive-year'),

    url(r'^$',
        Index.as_view(), name='events-index'),

    url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        Calendar.as_view(), name='events-calendar'),

)

ical_dict = {
    'ical_filename'              : 'calendar.ics',
    'last_modified_field'       : 'mod_date',
    'location_field'            : 'location',
    'start_time_field'          : 'start_time',
    'end_time_field'            : 'end_time',
}

urlpatterns += patterns('agenda.views.vobject_django',
    url(r'^calendar.ics$',
        'icalendar',     ical_dict,  name='agenda-icalendar'),
)
