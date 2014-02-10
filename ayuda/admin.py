#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from django.contrib import admin
from ayuda.models import Seccion
from ayuda.forms import SeccionForm


class SeccionAdmin(admin.ModelAdmin):

    form = SeccionForm

    class Media:

        js = ('/static/js/ckeditor/ckeditor.js',
              '/static/js/ckeditor/init.js')


admin.site.register(Seccion, SeccionAdmin)
