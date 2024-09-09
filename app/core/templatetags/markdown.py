from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code', 'codehilite'])

@register.filter()
@stringfilter
def lower(value):
    return str(value).lower()

@register.filter()
@stringfilter
def ticket_status(value):

    return str(value).lower().replace('(', '').replace(')', '').replace(' ', '_')

@register.filter()
@stringfilter
def date_time_seconds(value):

    return str(value).split('.')[0]
