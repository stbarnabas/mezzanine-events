from django import template
from django.template.defaultfilters import stringfilter
import re
from ..models import _get_current_domain, Event, EventContainer
from ..lib import get_utc
from django.utils.http import urlquote as quote
from mezzanine.conf import settings

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
	start_date = get_utc(event.start_datetime()).strftime("%Y%m%dT%H%M%SZ")
	end_date = get_utc(event.end_datetime()).strftime("%Y%m%dT%H%M%SZ")
	url = _get_current_domain() + event.get_absolute_url()
	location = quote(event.mappable_location)
	return "http://www.google.com/calendar/event?action=TEMPLATE&text={title}&dates={start_date}/{end_date}&sprop=website:{url}&location={location}&trp=true".format(**locals())

@register.filter(is_safe=True)
def google_nav_url(event):
	if not isinstance(event, Event):
		return ''
	location = quote(event.mappable_location)
	return "https://{}/maps?daddr={}".format(settings.MZEVENTS_GOOGLE_MAPS_DOMAIN, location)

@register.tag
def google_static_map(parser, token):
	try:
		tag_name, event, width, height, zoom = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError('google_static_map requires an event, width, height and zoom level')
	return GoogleStaticMapNode(event, width, height, zoom)

class GoogleStaticMapNode (template.Node):
	def __init__(self, e, w, h, z):
		self.event = template.Variable(e)
		self.width = w
		self.height = h
		self.zoom = z
	def render(self, context):
		event = self.event.resolve(context)
		width = self.width
		height = self.height
		zoom = self.zoom
		marker = quote('{:.6},{:.6}'.format(event.lat, event.lon))
		if settings.MZEVENTS_HIDPI_STATIC_MAPS:
			scale = 2
		else:
			scale = 1
		return "<img src='http://maps.googleapis.com/maps/api/staticmap?size={width}x{height}&scale={scale}&format=png&markers={marker}&sensor=false&zoom={zoom}' width='{width}' height='{height}' />".format(**locals())

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