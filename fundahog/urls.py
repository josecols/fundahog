#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols

from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', 'blog.views.index', name='blog'),
    url(r'^blog/pagina-(?P<pagina>\d+)/$', 'blog.views.index',
        name='blog_pagina'),
    url(r'^blog/entrada/(?P<slug>[-\w\d]+)-(?P<entrada_id>\d+)/$',
        'blog.views.entrada', name='entrada'),
    url(r'^blog/entrada/modificar/$', 'blog.views.modificar',
        name='modificar_entrada'),
    url(r'^blog/entrada/agregar/$', 'blog.views.agregar',
        name='agregar_entrada'),
    url(r'^blog/entrada/borrar/$', 'blog.views.borrar',
        name='borrar_entrada'),
    url(r'^blog/categoria/agregar/$', 'blog.views.agregar_categoria',
        name='agregar_categoria'),
    url(r'^blog/busqueda-(?P<pagina>\d+)/$', 'blog.views.busqueda',
        name='blog_busqueda'),
    url(r'^blog/busqueda-(?P<pagina>\d+)/(?P<query>[-\w]+)/$',
        'blog.views.busqueda', name='blog_busqueda_query'),
    url(r'^nosotros/$', 'portal.views.nosotros', name='nosotros'),
    url(r'^nosotros/(?P<slug>[-\w]+)$', 'portal.views.nosotros',
        name='nosotros_subseccion'),
    url(r'^programas/$', 'portal.views.programas', name='programas'),
    url(r'^contacto/$', 'portal.views.contacto', name='contacto'),
    url(r'^eventos/$', 'portal.views.eventos', name='eventos'),
    url(r'^eventos/pagina-(?P<pagina>\d+)/$', 'portal.views.eventos',
        name='eventos_pagina'),
    url(r'^eventos/evento/(?P<slug>[-\w\d]+)-(?P<evento_id>\d+)/$',
        'portal.views.evento', name='evento'),
    url(r'^eventos/evento/modificar/$', 'portal.views.modificar_evento'
        , name='modificar_evento'),
    url(r'^eventos/evento/agregar/$', 'portal.views.agregar_evento',
        name='agregar_evento'),
    url(r'^eventos/evento/borrar/$', 'portal.views.borrar_evento',
        name='borrar_evento'),
    url(r'^libros/$', 'portal.views.libros', name='libros'),
    url(r'^libros/pagina-(?P<pagina>\d+)/$', 'portal.views.libros',
        name='libros_pagina'),
    url(r'^libros/libro/(?P<slug>[-\w\d]+)-(?P<libro_id>\d+)/$',
        'portal.views.libro', name='libro'),
    url(r'^libros/libro/agregar/$', 'portal.views.agregar_libro',
        name='libro_agregar'),
    url(r'^libros/libro/modificar/$', 'portal.views.libro_modificar',
        name='libro_modificar'),
    url(r'^libros/libro/borrar/$', 'portal.views.borrar_libro',
        name='borrar_libro'),
    url(r'^libros/busqueda-(?P<pagina>\d+)/$',
        'portal.views.busqueda_libros', name='libros_busqueda'),
    url(r'^libros/busqueda-(?P<pagina>\d+)/(?P<query>[-\w]+)/$',
        'portal.views.busqueda_libros', name='libros_busqueda_query'),
    url(r'^libros/categoria/agregar/$', 'portal.views.agregar_categoria'
        , name='agregar_categoria_libros'),
    url(r'^galeria/$', 'portal.views.galeria', name='galeria'),
    url(r'^galeria/(?P<galeria_pk>\d+)/$', 'portal.views.galeria',
        name='galeria_pk'),
    url(r'^galerias/$', 'portal.views.galerias', name='galerias'),
    url(r'^albumes/$', 'portal.views.albumes', name='albumes'),
    url(r'^imagenes/$', 'portal.views.imagenes', name='imagenes'),
    url(r'^imagenes/imagen/agregar/$', 'portal.views.agregar_imagen',
        name='agregar_imagen'),
    url(r'^imagenes/imagen/borrar/$', 'portal.views.borrar_imagen',
        name='borrar_imagen'),
    )
