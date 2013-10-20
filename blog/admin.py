# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from django.contrib import admin
from blog.models import Categoria, Entrada

class EntradaAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/ckeditor/ckeditor.js',
              '/static/js/ckeditor/init.js',)
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'auto', None) is None:
            obj.autor = request.user
        obj.save()

admin.site.register(Categoria)
admin.site.register(Entrada, EntradaAdmin)
