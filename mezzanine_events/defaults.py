from mezzanine.conf import register_setting

register_setting(
	name="MZEVENTS_GOOGLE_MAPS_DOMAIN",
	description="The Google Maps country domain to geocode addresses with",
	editable=True,
	default="maps.google.com.au",
)