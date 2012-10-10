from mezzanine.pages.models import Page
from django.http import Http404, HttpResponse
from .models import Event, EventContainer, _get_current_domain
from icalendar import Calendar as ICalendar, Event as IEvent
from datetime import datetime
from . import __version__

def _make_icalendar():
	ical = ICalendar()
	ical.add('prodid',
		'-//St Barnabas Theological College/mezzanine-events//NONSGML V{}//EN'.format(__version__))
	ical.add('version', '2.0') # version of the format, not the product!
	return ical

def _make_ievent(ev):
	iev = IEvent()
	iev.add('summary', ev.title)
	iev.add('url', 'http://{domain}{url}'.format(
		domain=_get_current_domain(),
		url=ev.get_absolute_url(),
	))
	iev.add('location', ev.location)
	iev.add('dtstamp', datetime.combine(ev.date, ev.start_time))
	iev.add('dtstart', datetime.combine(ev.date, ev.start_time))
	iev.add('dtend', datetime.combine(ev.date, ev.end_time))
	iev['uid'] = "event-{id}@{domain}".format(
		id=ev.id,
		domain=_get_current_domain(),
	)
	return iev

def icalendar(request, slug):
	try:
		page = Page.objects.published(request.user).get(slug=slug)
	except Page.DoesNotExist:
		raise Http404()

	if not isinstance(page.get_content_model(), Event):
		raise Http404()

	ev = page.get_content_model()
	ical = _make_icalendar()
	iev = _make_ievent(ev)
	ical.add_component(iev)

	return HttpResponse(ical.to_ical(), content_type="text/calendar")

def icalendar_container(request, slug):
	try:
		page = Page.objects.published(request.user).get(slug=slug)
	except Page.DoesNotExist:
		raise Http404()

	if not isinstance(page.get_content_model(), EventContainer):
		raise Http404()

	ical = _make_icalendar()

	for child in page.children.all():
		if isinstance(child.get_content_model(), Event):
			ev = child.get_content_model()
			iev = _make_ievent(ev)
			ical.add_component(iev)

	return HttpResponse(ical.to_ical(), content_type="text/calendar")
