#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django import template
register = template.Library()


@register.filter(name='nombre_completo')
def nombre_completo(user):
    '''Retorna el nombre completo del usuario, si está establecido'''

    if user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    return unicode(user)


@register.filter(name='youtube_embed_url')
def youtube_embed_url(url):
    '''Convierte una URL de youtube a HTML embebido'''

    match = \
        re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$'
                  , url)
    if match:
        embed_url = 'http://www.youtube.com/embed/%s' % match.group(2)
        result = \
            '<div class="video-container"><iframe width="470" height="315" src="%s" frameborder="0" allowfullscreen></iframe></div>' \
            % embed_url
        return result
    return ''
youtube_embed_url.is_safe = True
