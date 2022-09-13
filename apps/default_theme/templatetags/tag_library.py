"""
Usage:
{% load json_tags %}
var = myJsObject = {{ template_var|to_json }};
Features:
- Built in support for dates, datetimes, lazy translations.
- Safe escaping of script tags.
- Support for including QuryDict objects.
- Support for custom serialization methods on objects via defining a `to_json()` method.
"""

import datetime
import json
import django.conf.global_settings as settings
from decimal import Decimal
from django import template
from django.http import QueryDict
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def to_int(value):
    return int(value)
