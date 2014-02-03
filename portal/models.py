#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

import uuid
import os
from PIL import Image
from django.db import models
from django.contrib.sites.models import Site
from django.db.models.signals import pre_delete
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify


def uuid_slug(uuid):
    return str(uuid)[:8]


def directorio(instance, nombre):
    if isinstance(instance, Evento):
        ruta = 'uploads/eventos'
    else:
        ruta = 'uploads/error'

    extension = nombre.split('.')[-1]
    nombre = '%s.%s' % (uuid_slug(uuid.uuid4()), extension)
    return os.path.join(ruta, nombre)


def redimensionar(archivo, ancho_requerido, alto_requerido):
    imagen = Image.open(archivo)
    (ancho, alto) = imagen.size
    if alto > alto_requerido and ancho > ancho_requerido:
        imagen.thumbnail((ancho_requerido, alto), Image.ANTIALIAS)
        imagen.save(archivo)


class Evento(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    contenido = models.TextField()
    portada = models.ImageField(upload_to=directorio)
    fecha = \
        models.DateTimeField(help_text='Formato de 24 horas. P. ej. 16:00'
                             )
    slug = models.SlugField(max_length=100, editable=False)

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Evento, self).save()
        if self.portada:
            archivo = self.portada.path
            redimensionar(archivo, 400, 200)


class Seccion(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    contenido = models.TextField()
    secciones = models.ManyToManyField('self', blank=True,
            verbose_name='Subsecciones',
            help_text='Toda subsección es integrada en la sección más general'
            )
    slug = models.SlugField(max_length=100, editable=False)
    creado = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:

        verbose_name = "sección"
        verbose_name_plural = 'secciones'

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Seccion, self).save()


class Telefono(models.Model):

    telefono = models.CharField(max_length=12, unique=True,
                                validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$'
                                , message='El formato es incorrecto')],
                                verbose_name="número de teléfono",
                                help_text='Formato XXX-XXX-XXXX. P. ej. 414-853-0463'
                                )
    principal = \
        models.BooleanField(help_text='Un número marcado como principal aparecerá en la cabecera del sitio'
                            )

    class Meta:

        verbose_name = "teléfono"
        verbose_name_plural = "teléfonos"

    def __unicode__(self):
        return self.telefono


class Correo(models.Model):

    correo = models.EmailField(verbose_name="Correo electrónico")

    def __unicode__(self):
        return str(self.correo)


class Organizacion(models.Model):

    site = models.OneToOneField(Site)
    direccion = models.TextField(verbose_name="dirección")
    telefonos = models.ManyToManyField(Telefono,
            verbose_name="números telefónicos")
    correos = models.ManyToManyField(Correo)
    twitter = models.URLField()
    facebook = models.URLField()

    class Meta:

        verbose_name = "organización"
        verbose_name_plural = "organización"

    def __unicode__(self):
        return "Información de la organización"


# Señales

def borrar_portada(sender, instance, **kwargs):
    if instance.portada:
        try:
            os.remove(instance.portada.path)
        except OSError:
            pass


pre_delete.connect(borrar_portada, sender=Evento)

