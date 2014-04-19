#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

import re

from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError


class Video(models.Model):
    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name='título')
    video = models.URLField(help_text='URL del vídeo en YouTube', verbose_name="vídeo")

    def __unicode__(self):
        return self.titulo

    def is_youtube_url(self):
        return re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(.*)(\&(.*))?$'
                         , self.video)

    def clean(self):
        super(Video, self).clean()
        if self.video and not self.is_youtube_url():
            raise ValidationError("La URL del vídeo no es válida.")


class Seccion(models.Model):
    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name='título')
    contenido = models.TextField()
    videos = models.ManyToManyField(Video, verbose_name='videos')
    archivo = models.FileField(upload_to='uploads/ayuda', blank=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    editado = models.DateField(editable=False, auto_now=True)

    class Meta:

        verbose_name = 'sección'
        verbose_name_plural = 'secciones'

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Seccion, self).save()

    def clean(self):
        super(Seccion, self).clean()
        if self.archivo:
            extension = self.archivo.name.split('.')[-1].lower()
            if extension != 'pdf':
                raise ValidationError('El archivo debe ser del tipo PDF.')


