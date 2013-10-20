# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from django.db import models
from django.template.defaultfilters import slugify


class Evento(models.Model):
    titulo = models.CharField(max_length=100, unique=True, verbose_name="título")
    contenido = models.TextField()
    portada = models.ImageField(upload_to='uploads/eventos/portadas')
    fecha = models.DateTimeField(help_text='Formato de 24 horas. P. ej. 16:00')
    slug = models.SlugField(max_length=100, editable=False)    
    
    def __unicode__(self):
        return self.titulo    
    
    def save(self): 
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Evento, self).save()
