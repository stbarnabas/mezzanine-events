from mezzanine.conf import settings
from django.utils import timezone as tz
import pytz

def get_utc(datetime):
	if settings.MZEVENTS_TIME_ZONE != "":
		app_tz = pytz.timezone(settings.MZEVENTS_TIME_ZONE)
	else:
		app_tz = tz.get_default_timezone()
	
	# make the datetime aware
	if tz.is_naive(datetime):
		datetime = tz.make_aware(datetime, app_tz)
	
	# now, make it UTC
	datetime = tz.make_naive(datetime, tz.utc)
	
	return datetime