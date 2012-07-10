from mezzanine.pages.models import Page
from django.http import Http404, HttpResponse
from .models import Event
from icalendar import Calendar as ICalendar, Event as IEvent
from datetime import datetime

def icalendar(request, slug):
	try:
		page = Page.objects.published(request.user).get(slug=slug)
	except Page.DoesNotExist:
		raise Http404()

	if not isinstance(page.get_content_model(), Event):
		raise Http404()

	ev = page.get_content_model()

	ical = ICalendar()
	ical.add('prodid', 'au.com.anglican.adelaide.mezzanine.calendar')
	ical.add('version', '2.0')
	iev = IEvent()
	iev.add('summary', ev.title)
	iev.add('url', 'http://sbtc.org.au{}'.format(ev.get_absolute_url()))
	iev.add('location', ev.location)
	iev.add('dtstamp', datetime.combine(ev.date, ev.start_time))
	iev.add('dtstart', datetime.combine(ev.date, ev.start_time))
	iev.add('dtend', datetime.combine(ev.date, ev.end_time))
	iev['uid'] = "evt-{}@sbtc.org.au".format(ev.id)
	ical.add_component(iev)

	return HttpResponse(ical.to_ical(), content_type="text/calendar")
	
	