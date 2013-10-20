# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
import uuid, os
from PIL import Image
from django.db import models
from django.template.defaultfilters import slugify

def directorio(instance, nombre):
    if isinstance(instance, Evento):
        ruta = 'uploads/eventos'
    else:
        ruta = 'uploads/error'
        
    extension = nombre.split('.')[-1]
    nombre = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join(ruta, nombre)

def redimensionar(archivo, ancho_requerido, alto_requerido):
    imagen = Image.open(archivo)
    ancho, alto = imagen.size
    if alto > alto_requerido and ancho > ancho_requerido:
        imagen.thumbnail((ancho_requerido, alto), Image.ANTIALIAS)
        imagen.save(archivo)  
         
class Evento(models.Model):
    titulo = models.CharField(max_length=100, unique=True, verbose_name="título")
    contenido = models.TextField()
    portada = models.ImageField(upload_to=directorio)
    fecha = models.DateTimeField(help_text='Formato de 24 horas. P. ej. 16:00')
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
                
                
