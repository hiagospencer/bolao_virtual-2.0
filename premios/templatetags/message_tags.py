from django import template
from ..utils import MessageSystem

register = template.Library()

@register.simple_tag(takes_context=True)
def get_custom_messages(context):
    request = context['request']
    return MessageSystem.get_messages(request)

@register.filter
def message_class(message_type):
    classes = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }
    return classes.get(message_type, '')
