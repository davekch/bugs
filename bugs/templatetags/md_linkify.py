import re
from django import template
register = template.Library()

@register.filter
def markdown_linkify(text):
    """replaces links with []()-style markdown links
    """
    urlmatch = r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)"
    return re.sub(urlmatch, r"[\1](\1)", text)

