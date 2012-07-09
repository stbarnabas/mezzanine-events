from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText
from django.core.exceptions import ValidationError
from geopy.geocoders import Google as GoogleMaps
from geopy.geocoders.google import GQueryError
from django.contrib.sites.models import Site
from urllib import quote
from datetime import timedelta, datetime as dt

UTC_DELTA = timedelta(hours=9, minutes=30)

class Event(Page, RichText):
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	speakers = models.TextField(blank=True, help_text="Leave blank if not relevant. Write one name per line.")
	location = models.TextField()
	mappable_location = models.CharField(max_length=128, blank=True, help_text="This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.")
	lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Latitude", help_text="Calculated automatically if mappable location is set.")
	lon = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Longitude", help_text="Calculated automatically if mappable location is set.")
	rsvp = models.TextField(blank=True)

	def speakers_dict(self):
		return [x for x in self.speakers.split("\n") if x.strip() != ""]

	def start_datetime(self):
		return dt.combine(self.date, self.start_time)

	def end_datetime(self):
		return dt.combine(self.date, self.end_time)

	def build_webcal_url(self):
		return "webcal://"+Site.objects.get_current().domain+self.get_absolute_url()+"event.ics"

	def build_icalendar_url(self):
		return "http://"+Site.objects.get_current().domain+self.get_absolute_url()+"event.ics"

	def build_google_calendar_url(self):
		# from sbtc.events.models import Event; Event.objects.all()[0].build_google_calendar_url()
		title = quote(self.title)
		start_date = (self.start_datetime() - UTC_DELTA).strftime("%Y%m%dT%H%M%SZ")
		end_date = (self.end_datetime() - UTC_DELTA).strftime("%Y%m%dT%H%M%SZ")
		url = Site.objects.get_current().domain+self.get_absolute_url()
		location = quote(self.mappable_location)
		return "http://www.google.com/calendar/event?action=TEMPLATE&text={title}&dates={start_date}/{end_date}&sprop=website:{url}&location={location}&trp=true".format(**locals())


	def clean(self):
		super(Event, self).clean()

		if not self.parent or (isinstance(self.parent.get_content_model(), EventContainer) and self.parent.get_content_model().hide_children):
			self.in_navigation = False

		if self.lat and not self.lon:
			raise ValidationError("Longitude required if specifying latitude.")

		if self.lon and not self.lat:
			raise ValidationError("Latitude required if specifying longitude.")

		if not (self.lat and self.lon) and not self.mappable_location:
			self.mappable_location = self.location.replace("\n",", ")

		if self.mappable_location: #location should always override lat/long if set
			g = GoogleMaps(domain="maps.google.com.au")
			try:
				location, (lat, lon) = g.geocode(self.mappable_location)
			except GQueryError as e:
				raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any businessnames, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
			self.mappable_location = location
			self.lat = lat
			self.lon = lon

	class Meta:
		verbose_name = "Event"

class EventContainer (Page):
	hide_children = models.BooleanField(default=True, verbose_name="Hide events in this container from navigation")
	class Meta:
		verbose_name = "Event Container"
