from django import template
from django.template.defaultfilters import stringfilter
import re
from ..models import _get_current_domain, UTC_DELTA, Event, EventContainer
from urllib import quote

register = template.Library()

myre = re.compile(r'([a-zA-Z0-9\-\.\_]+@[a-zA-Z0-9\-\.\_]+\.[a-zA-Z0-9\-\.\_]+)')

@register.filter(is_safe=True)
@stringfilter
def link_emails(value):
	return myre.sub("<a href='mailto:\\1'>\\1</a>", value)

@register.filter(is_safe=True)
def google_calendar_url(event):
	if not isinstance(event, Event):
		return ''
	title = quote(event.title)
	start_date = (event.start_datetime() - UTC_DELTA).strftime("%Y%m%dT%H%M%SZ")
	end_date = (event.end_datetime() - UTC_DELTA).strftime("%Y%m%dT%H%M%SZ")
	url = _get_current_domain() + event.get_absolute_url()
	location = quote(event.mappable_location)
	return "http://www.google.com/calendar/event?action=TEMPLATE&text={title}&dates={start_date}/{end_date}&sprop=website:{url}&location={location}&trp=true".format(**locals())

@register.filter(is_safe=True)
def icalendar_url(obj, proto_param=None):
	if proto_param is None:
		proto = 'http://'
	else:
		proto = '{}://'.format(proto_param)
	if isinstance(obj, Event):
		endfile = 'event.ics'
	elif isinstance(obj, EventContainer):
		endfile = 'calendar.ics'
	else:
		return obj
	return proto + _get_current_domain() + obj.get_absolute_url() + endfile