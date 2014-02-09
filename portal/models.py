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
    elif isinstance(instance, Imagen):
        ruta = 'uploads/imagenes'
    elif isinstance(instance, Libro):
        ruta = 'uploads/libros/portadas'
    elif isinstance(instance, Programa):
        ruta = 'uploads/programas/portadas'
    else:
        ruta = 'uploads/error'

    extension = nombre.split('.')[-1]
    nombre = '%s.%s' % (uuid_slug(uuid.uuid4()), extension)
    return os.path.join(ruta, nombre)


def redimensionar(
    archivo,
    ancho_requerido,
    alto_requerido,
    archivo_salida=None,
    ):

    imagen = Image.open(archivo)
    (ancho, alto) = imagen.size
    if alto > alto_requerido and ancho > ancho_requerido:
        imagen.thumbnail((ancho_requerido, alto), Image.ANTIALIAS)
        if archivo_salida:
            imagen.save(archivo_salida)
        else:
            imagen.save(archivo)


def thumbnail(archivo, ancho_requerido, alto_requerido):
    thumb = os.path.splitext(archivo)[0] + '.thumbnail' \
        + os.path.splitext(archivo)[1]
    redimensionar(archivo, ancho_requerido, alto_requerido, thumb)
    return thumb


class Evento(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    contenido = models.TextField()
    portada = models.ImageField(upload_to=directorio)
    fecha = \
        models.DateTimeField(help_text='Formato de 24 horas. P. ej. 16:00.'
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
            help_text='Toda subsección es integrada en la sección más general.'
            )
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    creado = models.DateField(editable=False, auto_now_add=True)

    class Meta:

        verbose_name = "sección"
        verbose_name_plural = 'secciones'

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Seccion, self).save()


class Imagen(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    imagen = models.ImageField(upload_to=directorio)
    thumbnail = models.CharField(max_length=255, editable=False)

    class Meta:

        verbose_name = 'imagen'
        verbose_name_plural = 'imágenes'

    def __unicode__(self):
        return self.titulo

    def save(self):
        super(Imagen, self).save()
        if self.imagen:
            archivo = self.imagen.path
            redimensionar(archivo, 1024, 768)
            self.thumbnail = 'uploads/imagenes/' \
                + os.path.basename(thumbnail(archivo, 200, 200))
            super(Imagen, self).save()


class Album(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    imagenes = models.ManyToManyField(Imagen, verbose_name='imágenes')
    creado = models.DateField(editable=False, auto_now_add=True)

    class Meta:

        verbose_name = "álbum"
        verbose_name_plural = 'álbumes'

    def __unicode__(self):
        return self.titulo


class Galeria(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    albumes = models.ManyToManyField(Album, verbose_name='álbumes')

    def __unicode__(self):
        return self.titulo


class Telefono(models.Model):

    telefono = models.CharField(max_length=12, unique=True,
                                validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$'
                                , message='El formato es incorrecto')],
                                verbose_name="número de teléfono",
                                help_text='Formato XXX-XXX-XXXX. P. ej. 414-853-0463'
                                )
    principal = \
        models.BooleanField(help_text='Un número marcado como principal aparecerá en la cabecera del sitio.'
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

    def __str__(self):
        return "Información de la organización"


class Categoria(models.Model):

    descripcion = models.CharField(max_length=100, unique=True,
                                   verbose_name='descripción')
    slug = models.SlugField(max_length=100, editable=False)

    class Meta:

        verbose_name = "categoría"
        verbose_name_plural = 'categorías'

    def __unicode__(self):
        return self.descripcion

    def save(self):
        if not self.id:
            self.slug = slugify(self.descripcion)
        super(Categoria, self).save()


class Libro(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    descripcion = models.TextField(max_length=255,
                                   verbose_name='descripción')
    categorias = models.ManyToManyField(Categoria,
            verbose_name='categorías')
    portada = models.ImageField(upload_to=directorio)
    archivo = models.FileField(upload_to='uploads/libros')
    slug = models.SlugField(max_length=100, editable=False)

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Libro, self).save()
        if self.portada:
            archivo = self.portada.path
            redimensionar(archivo, 400, 200)


class Programa(models.Model):

    titulo = models.CharField(max_length=100, unique=True,
                              verbose_name="título")
    contenido = models.TextField()
    portada = models.ImageField(upload_to=directorio)
    archivo = models.FileField(upload_to='uploads/programas',
                               blank=True)
    slug = models.SlugField(max_length=100, editable=False)

    def __unicode__(self):
        return self.titulo

    def save(self):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Programa, self).save()
        if self.portada:
            archivo = self.portada.path
            redimensionar(archivo, 400, 200)


# Señales

def borrar_portada(sender, instance, **kwargs):
    if instance.portada:
        try:
            os.remove(instance.portada.path)
        except OSError:
            pass


def borrar_archivo(sender, instance, **kwargs):
    if instance.archivo:
        try:
            os.remove(instance.archivo.path)
        except OSError:
            pass


def borrar_imagen(sender, instance, **kwargs):
    if instance.imagen:
        try:
            os.remove(instance.imagen.path)
        except OSError:
            pass
    if instance.thumbnail:
        try:
            os.remove(instance.thumbnail)
        except OSError:
            pass


pre_delete.connect(borrar_portada, sender=Evento)
pre_delete.connect(borrar_portada, sender=Programa)
pre_delete.connect(borrar_portada, sender=Libro)
pre_delete.connect(borrar_archivo, sender=Libro)
pre_delete.connect(borrar_archivo, sender=Programa)
pre_delete.connect(borrar_imagen, sender=Imagen)

