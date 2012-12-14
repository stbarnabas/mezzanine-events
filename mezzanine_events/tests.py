"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals

from django.test import TestCase
from .models import Event
from datetime import date, time


class EventTests (TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            date=date.today(),
            start_time=time(9),
            end_time=time(17,30),
            speakers='Fred\nJoe',
            location='1 Susan St\nHindmarsh\nSouth Australia',
            rsvp='By 31 December to aaa@bbb.com',
        )
        self.unicode_event = Event.objects.create(
            date=date.today(),
            start_time=time(9),
            end_time=time(17,30),
            location='\u30b5\u30f3\u30b7\u30e3\u30a4\u30f360', # Japanese for 'Sunshine 60', a skyscraper in Tokyo
        )
    
    def test_speakers_list(self):
        self.assertEqual(self.event.speakers_list(), ['Fred', 'Joe'])
    
    def test_clean(self):
        self.event.clean()
        self.assertAlmostEqual(self.event.lat, -34.907924, places=5)
        self.assertAlmostEqual(self.event.lon, 138.567624, places=5)
        self.assertEqual(self.event.mappable_location, '1 Susan St, Hindmarsh SA 5007, Australia')
        
        self.unicode_event.clean()
        self.assertAlmostEqual(self.unicode_event.lat, 35.729534, places=5)
        self.assertAlmostEqual(self.unicode_event.lon, 139.718055, places=5)
        self.assertEqual(self.unicode_event.mappable_location, 'Japan, \u3012170-6090 Tokyo, Toshima, Higashiikebukuro, \uff13\u4e01\u76ee\uff11 \u30b5\u30f3\u30b7\u30e3\u30a4\u30f3\uff16\uff10')
    
    def test_urls(self):
