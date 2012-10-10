from setuptools import setup
import os
from mezzanine_events import __version__

setup(name='mezzanine-events',
	version=__version__,
	description='Event pages for the Mezzanine CMS',
	author='Adam Brenecki',
	author_email='abrenecki@sbtc.org.au',
	url='https://github.com/stbarnabas/mezzanine-events',
	packages=['.'.join(i[0].split(os.sep))
		for i in os.walk('mezzanine_events')
		if '__init__.py' in i[2]],
	install_requires=[
		'icalendar==3.0.1b2',
		'geopy==0.94.2',
		'pytz',
	]
)
