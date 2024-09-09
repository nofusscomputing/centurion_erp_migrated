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


@register.filter()
@stringfilter
def to_duration(value):
    """Convert seconds to duration value

    Args:
        value (str): Time in seconds

    Returns:
        str: Duration value in format 00h 00m 00s
    """

    hours = int(int(value)//3600)

    minutes = int((int(value)%3600)//60)

    seconds = int((int(value)%3600)%60)

    return str("{:02d}h {:02d}m {:02d}s".format(hours, minutes, seconds))
