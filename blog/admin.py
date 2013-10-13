# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from django.contrib import admin
from blog.models import Entrada

class EntradaAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/ckeditor/ckeditor.js',
              '/static/js/ckeditor/init.js',)

admin.site.register(Entrada, EntradaAdmin)