#encoding:utf-8
from django import template
register = template.Library()

# Retorna el nombre completo del usuario, si está establecido
@register.filter(name='nombre_completo')
def nombre_completo(user):
    if (user.first_name and user.last_name):
        return "%s %s" % (user.first_name, user.last_name)
    return unicode(user)