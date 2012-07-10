
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns("",
    url("^(?P<slug>.*)/event.ics$", views.icalendar),
    url("^(?P<slug>.*)/calendar.ics$", views.icalendar_container),
)
