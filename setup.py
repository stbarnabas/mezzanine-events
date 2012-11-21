from setuptools import setup
import os
from mezzanine_events import __version__
import subprocess

def get_long_desc():
	"""Use Pandoc to convert the readme to ReST for the PyPI."""
	try:
		return subprocess.check_output(['pandoc', '-f', 'markdown', '-t', 'rst', 'README.mdown'])
	except:
		print "WARNING: The long readme wasn't converted properly"

setup(name='mezzanine-events',
	version=__version__,
	description='Event pages for the Mezzanine CMS',
	long_description=get_long_desc(),
	author='Adam Brenecki',
	author_email='abrenecki@sbtc.org.au',
	url='https://github.com/stbarnabas/mezzanine-events',
	packages=['.'.join(i[0].split(os.sep))
		for i in os.walk('mezzanine_events')
		if '__init__.py' in i[2]],
	package_dir={'.'.join(i[0].split(os.sep)): i[0]
		for i in os.walk('mezzanine_events')
		if '__init__.py' in i[2]},
	package_data={
		'mezzanine_events': ['templates/**'],
	},
	install_requires=[
		'icalendar==3.0.1b2',
		'geopy==0.94.2',
		'pytz',
	],
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Framework :: Django',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)