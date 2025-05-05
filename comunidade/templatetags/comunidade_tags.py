from django import template
from ..models import Enquete

register = template.Library()

@register.filter(name='ja_votou')
def ja_votou_filter(enquete, user):
    """Template tag para verificar se usuário já votou"""
    return enquete.usuario_ja_votou(user)

@register.filter(name='voto_usuario')
def voto_usuario_filter(enquete, user):
    """Template tag para obter o voto do usuário"""
    return enquete.get_voto_usuario(user)
