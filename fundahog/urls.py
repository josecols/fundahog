# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, }),
    url(r'^$', 'blog.views.index', name='blog'),
    url(r'^entrada/(?P<slug>[-\w\d]+)-(?P<entrada_id>\d+)/$', 'blog.views.entrada' , name='entrada'),
    url(r'^entrada/modificar/$', 'blog.views.modificar' , name='modificar_entrada'),
    url(r'^entrada/agregar/$', 'blog.views.agregar' , name='agregar_entrada'),
)
