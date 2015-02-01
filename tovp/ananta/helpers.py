import re
import datetime

from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from jingo import register
from jinja2 import Markup
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.html import strip_tags
from django.utils.timesince import timesince

from num2words import num2words as _num2words
from markdown import markdown


register.filter(timesince)


@register.function
def static(path):
    return staticfiles_storage.url(path)


@register.function
def now(format="%d %B %Y"):
    return datetime.date.today().strftime(format)


@register.function
def active_link_class(request, pattern):
    if re.search(pattern, request.path):
        return Markup(' active')
    return ''


@register.filter()
def add_css(field, css_class, *args, **kwargs):
    return field.as_widget(attrs={"class": css_class})


re_digits_nondigits = re.compile(r'\d+|\D+')


@register.filter
def format_with_commas(value, format='%i'):
    """
    >>> format_with_commas('%.4f', .1234)
    '0.1234'
    >>> format_with_commas('%i', 100)
    '100'
    >>> format_with_commas('%.4f', 234.5678)
    '234.5678'
    >>> format_with_commas('$%.4f', 234.5678)
    '$234.5678'
    >>> format_with_commas('%i', 1000)
    '1,000'
    >>> format_with_commas('%.4f', 1234.5678)
    '1,234.5678'
    >>> format_with_commas('$%.4f', 1234.5678)
    '$1,234.5678'
    >>> format_with_commas('%i', 1000000)
    '1,000,000'
    >>> format_with_commas('%.4f', 1234567.5678)
    '1,234,567.5678'
    >>> format_with_commas('$%.4f', 1234567.5678)
    '$1,234,567.5678'
    >>> format_with_commas('%i', -100)
    '-100'
    >>> format_with_commas('%.4f', -234.5678)
    '-234.5678'
    >>> format_with_commas('$%.4f', -234.5678)
    '$-234.5678'
    >>> format_with_commas('%i', -1000)
    '-1,000'
    >>> format_with_commas('%.4f', -1234.5678)
    '-1,234.5678'
    >>> format_with_commas('$%.4f', -1234.5678)
    '$-1,234.5678'
    >>> format_with_commas('%i', -1000000)
    '-1,000,000'
    >>> format_with_commas('%.4f', -1234567.5678)
    '-1,234,567.5678'
    >>> format_with_commas('$%.4f', -1234567.5678)
    '$-1,234,567.5678'
    """
    def _commafy(s):
        r = []
        for i, c in enumerate(reversed(s)):
            if i and (not (i % 3)):
                r.insert(0, ',')
            r.insert(0, c)
        return ''.join(r)

    parts = re_digits_nondigits.findall(format % (value,))
    for i in range(len(parts)):
        s = parts[i]
        if s.isdigit():
            parts[i] = _commafy(s)
            break
    return ''.join(parts)


@register.filter
def format_for_india(value):
    """
    >>> format_for_india(.1234)
    '0.1234'
    """
    return re.sub(r"(?<=\d)(?=(\d{2}){0,2}\d{3}(\d{7})*(?!\d))", ",",
                  str(value))


@register.filter
def datetimeformat(value, format='%d %B %Y'):
    return value.strftime(format)


@register.filter
def num2words(value):
    return _num2words(value)


@register.filter
def makeplain(value, trim_if=160, trim_on=150):
    text = strip_tags(markdown(value))
    if len(text) > trim_if:
        text = text[:trim_on].strip() + '...'
    return text


@register.filter
def update_url_query(url, dictionary):
    parsed = urlparse(url)
    data = parse_qs(parsed.query)
    for name, value in dictionary.items():
        if value is not None:
            data.update({
                name: [value],
            })
        else:
            if name in data:
                del data[name]

    _data = []
    for key, value in sorted(data.items()):
        for item in value:
            _data.append((key, item))

    return urlunparse([parsed.scheme, parsed.netloc, parsed.path,
                       parsed.params, urlencode(_data),
                       parsed.fragment])
