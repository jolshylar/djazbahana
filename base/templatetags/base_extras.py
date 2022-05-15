import markdown
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_markdown(text):
    return markdown.markdown(text, extensions=["markdown.extensions.fenced_code"])
