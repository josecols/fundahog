#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from django.contrib import admin
from portal.models import Evento, Seccion, Telefono, Correo, \
    Organizacion, Imagen, Album, Galeria, Libro, Categoria, Programa, \
    Mensaje
from portal.forms import EventoForm, SeccionForm, ProgramaForm


class EventoAdmin(admin.ModelAdmin):

    form = EventoForm

    class Media:

        js = ('/static/js/ckeditor/ckeditor.js',
              '/static/js/ckeditor/init.js')


class SeccionAdmin(admin.ModelAdmin):

    form = SeccionForm

    class Media:

        js = ('/static/js/ckeditor/ckeditor.js',
              '/static/js/ckeditor/init.js')


class ProgramaAdmin(admin.ModelAdmin):

    form = ProgramaForm

    class Media:

        js = ('/static/js/ckeditor/ckeditor.js',
              '/static/js/ckeditor/init.js')


admin.site.register(Evento, EventoAdmin)
admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Telefono)
admin.site.register(Correo)
admin.site.register(Organizacion)
admin.site.register(Imagen)
admin.site.register(Album)
admin.site.register(Galeria)
admin.site.register(Libro)
admin.site.register(Categoria)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Mensaje)
