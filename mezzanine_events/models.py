from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText
from django.core.exceptions import ValidationError
from geopy.geocoders import Google as GoogleMaps
from geopy.geocoders.google import GQueryError
from django.contrib.sites.models import Site
from datetime import timedelta, datetime as dt
from mezzanine.utils.sites import current_site_id
from mezzanine.conf import settings

def _get_current_domain():
	return Site.objects.get(id=current_site_id()).domain

class Event(Page, RichText):
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	speakers = models.TextField(blank=True, help_text="Leave blank if not relevant. Write one name per line.")
	location = models.TextField()
	mappable_location = models.CharField(max_length=128, blank=True, help_text="This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.")
	lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Latitude", help_text="Calculated automatically if mappable location is set.")
	lon = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Longitude", help_text="Calculated automatically if mappable location is set.")
	rsvp = models.TextField(blank=True, help_text="RSVP information. Leave blank if not relevant. Emails will be converted into links.")

	def speakers_list(self):
		return [x for x in self.speakers.split("\n") if x.strip() != ""]

	def start_datetime(self):
		return dt.combine(self.date, self.start_time)

	def end_datetime(self):
		return dt.combine(self.date, self.end_time)

	def clean(self):
		super(Event, self).clean()

		if self.lat and not self.lon:
			raise ValidationError("Longitude required if specifying latitude.")

		if self.lon and not self.lat:
			raise ValidationError("Latitude required if specifying longitude.")

		if not (self.lat and self.lon) and not self.mappable_location:
			self.mappable_location = self.location.replace("\n",", ")

		if self.mappable_location: #location should always override lat/long if set
			g = GoogleMaps(domain=settings.MZEVENTS_GOOGLE_MAPS_DOMAIN)
			try:
				location, (lat, lon) = g.geocode(self.mappable_location.encode('utf-8'))
			except GQueryError as e:
				raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
			except ValueError as e:
				raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
			self.mappable_location = location
			self.lat = lat
			self.lon = lon
		
	def save(self, *args, **kwargs):
		# determine whether the page needs to be hidden
		# this has to be done here because we don't have access to the parent in clean()
		hide_page = False
				
		if self.parent is not None:
			hide_page = isinstance(self.parent.get_content_model(), EventContainer) and self.parent.get_content_model().hide_children
		
		if hide_page:
			# older versions
			self.in_navigation = False
			# newer versions
			self.in_menus = ""
		
		super(Event, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Event"

class EventContainer (Page):
	hide_children = models.BooleanField(default=True, verbose_name="Hide events in this container from navigation")
	class Meta:
		verbose_name = "Event Container"
