# home/templatetags/seo_extras.py
from django import template
from urllib.parse import urlparse, urlunparse

register = template.Library()

@register.filter
def cut_querystring(url):
    """Return url without query string or fragment."""
    if not url:
        return url
    parts = urlparse(url)
    return urlunparse((parts.scheme, parts.netloc, parts.path, '', '', ''))