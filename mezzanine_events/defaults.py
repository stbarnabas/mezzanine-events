from mezzanine.conf import register_setting

register_setting(
	name="MZEVENTS_GOOGLE_MAPS_DOMAIN",
	description="The Google Maps country domain to geocode addresses with",
	editable=True,
	default="maps.google.com.au",
)

register_setting(
	name="MZEVENTS_TIME_ZONE",
	description="The timezone that event times are written in, if different from the timezone in settings.TIME_ZONE",
	editable=True,
	default="",
)

register_setting(
	name="MZEVENTS_HIDPI_STATIC_MAPS",
	description="Generate maps suitable for Retina displays",
	editable=True,
	default=True,
)