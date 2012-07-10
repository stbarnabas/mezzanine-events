from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

myre = re.compile(r'([a-zA-Z0-9\-\.\_]+@[a-zA-Z0-9\-\.\_]+\.[a-zA-Z0-9\-\.\_]+)')

@register.filter(is_safe=True)
@stringfilter
def link_emails(value):
	return myre.sub(
		"<a href='mailto:\\1'>\\1</a>", 
		value)