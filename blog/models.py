#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Categoria(models.Model):

    descripcion = models.CharField(max_length=100, unique=True,
                                   verbose_name="descripción")
    slug = models.SlugField(max_length=100, editable=False)

    class Meta:

        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __unicode__(self):
        return self.descripcion

    def save(self):
        if not self.id:
            self.slug = slugify(self.descripcion)
        super(Categoria, self).save()


class Entrada(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    contenido = models.TextField()
    categorias = models.ManyToManyField(Categoria)
    importante = \
        models.BooleanField(help_text='Una entrada marcada como importante aparecerá en todo el sitio.'
                            )
    autor = models.ForeignKey(User, editable=False)
    slug = models.SlugField(max_length=100, editable=False)
    creado = models.DateTimeField(editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Entrada, self).save()


