from setuptools import setup

setup(name='mezzanine-events',
	version='0.1pre',
	description='Event pages for the Mezzanine CMS',
	author='Adam Brenecki',
	author_email='abrenecki@sbtc.org.au',
	url='https://github.com/stbarnabas/mezzanine-events',
	packages=[
		'mezzanine_events',
		'mezzanine_events.migrations',
		'mezzanine_events.templatetags',
	],
	install_requires=[
		'icalendar==3.0.1b2'
	]
)
