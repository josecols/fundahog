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
    url(r'^blog/entrada/importante/$', 'blog.views.entrada_importante',
        name='entrada_importante'),
    url(r'^blog/entrada/agregar/$', 'blog.views.entrada_agregar',
        name='entrada_agregar'),
    url(r'^blog/entrada/modificar/$', 'blog.views.entrada_modificar',
        name='entrada_modificar'),
    url(r'^blog/entrada/borrar/$', 'blog.views.entrada_borrar',
        name='entrada_borrar'),
    url(r'^blog/categoria/agregar/$', 'blog.views.categoria_agregar',
        name='categoria_agregar'),
    url(r'^blog/busqueda-(?P<pagina>\d+)/$', 'blog.views.busqueda',
        name='blog_busqueda'),
    url(r'^blog/busqueda-(?P<pagina>\d+)/(?P<query>[-\w]+)/$',
        'blog.views.busqueda', name='blog_busqueda_query'),
    url(r'^nosotros/$', 'portal.views.nosotros', name='nosotros'),
    url(r'^nosotros/(?P<slug>[-\w]+)/$', 'portal.views.nosotros',
        name='nosotros_subseccion'),
    url(r'^secciones/seccion/(?P<slug>[-\w]+)/$', 'portal.views.seccion'
        , name='seccion'),
    url(r'^secciones/seccion/agregar$', 'portal.views.seccion_agregar',
        name='seccion_agregar'),
    url(r'^secciones/seccion/modificar$',
        'portal.views.seccion_modificar', name='seccion_modificar'),
    url(r'^secciones/seccion/borrar$', 'portal.views.seccion_borrar',
        name='seccion_borrar'),
    url(r'^programas/$', 'portal.views.programas', name='programas'),
    url(r'^programas/pagina-(?P<pagina>\d+)/$', 'portal.views.programas'
        , name='programas_pagina'),
    url(r'^programas/programa/(?P<slug>[-\w\d]+)-(?P<programa_id>\d+)/$'
        , 'portal.views.programa', name='programa'),
    url(r'^programas/programa/agregar$', 'portal.views.programa_agregar'
        , name='programa_agregar'),
    url(r'^programas/programa/modificar$',
        'portal.views.programa_modificar', name='programa_modificar'),
    url(r'^programas/programa/borrar$', 'portal.views.programa_borrar',
        name='programa_borrar'),
    url(r'^contacto/$', 'portal.views.contacto', name='contacto'),
    url(r'^eventos/$', 'portal.views.eventos', name='eventos'),
    url(r'^eventos/pagina-(?P<pagina>\d+)/$', 'portal.views.eventos',
        name='eventos_pagina'),
    url(r'^eventos/evento/(?P<slug>[-\w\d]+)-(?P<evento_id>\d+)/$',
        'portal.views.evento', name='evento'),
    url(r'^eventos/evento/agregar/$', 'portal.views.evento_agregar',
        name='evento_agregar'),
    url(r'^eventos/evento/modificar/$', 'portal.views.evento_modificar'
        , name='evento_modificar'),
    url(r'^eventos/evento/borrar/$', 'portal.views.evento_borrar',
        name='evento_borrar'),
    url(r'^libros/$', 'portal.views.libros', name='libros'),
    url(r'^libros/pagina-(?P<pagina>\d+)/$', 'portal.views.libros',
        name='libros_pagina'),
    url(r'^libros/libro/(?P<slug>[-\w\d]+)-(?P<libro_id>\d+)/$',
        'portal.views.libro', name='libro'),
    url(r'^libros/libro/agregar/$', 'portal.views.libro_agregar',
        name='libro_agregar'),
    url(r'^libros/libro/modificar/$', 'portal.views.libro_modificar',
        name='libro_modificar'),
    url(r'^libros/libro/borrar/$', 'portal.views.libro_borrar',
        name='libro_borrar'),
    url(r'^libros/busqueda-(?P<pagina>\d+)/$',
        'portal.views.libros_busqueda', name='libros_busqueda'),
    url(r'^libros/busqueda-(?P<pagina>\d+)/(?P<query>[-\w]+)/$',
        'portal.views.libros_busqueda', name='libros_busqueda_query'),
    url(r'^libros/categoria/agregar/$', 'portal.views.categoria_agregar'
        , name='libros_categoria_agregar'),
    url(r'^galeria/$', 'portal.views.galeria', name='galeria'),
    url(r'^galeria/(?P<galeria_pk>\d+)/$', 'portal.views.galeria',
        name='galeria_pk'),
    url(r'^galerias/$', 'portal.views.galerias', name='galerias'),
    url(r'^albumes/$', 'portal.views.albumes', name='albumes'),
    url(r'^imagenes/$', 'portal.views.imagenes', name='imagenes'),
    url(r'^imagenes/imagen/agregar/$', 'portal.views.imagen_agregar',
        name='imagen_agregar'),
    url(r'^imagenes/imagen/borrar/$', 'portal.views.imagen_borrar',
        name='imagen_borrar'),
    url(r'^ayuda/$', 'ayuda.views.ayuda', name='ayuda'),
    url(r'^ayuda/seccion/(?P<slug>[-\w\d]+)-(?P<seccion_id>\d+)/$',
        'ayuda.views.ayuda', name='ayuda_seccion'),
    )
