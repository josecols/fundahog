# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
import uuid, os
from PIL import Image
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_delete

def uuid_slug(uuid):
    return str(uuid)[:8]

def directorio(instance, nombre):
    if isinstance(instance, Evento):
        ruta = 'uploads/eventos'
    else:
        ruta = 'uploads/error'
        
    extension = nombre.split('.')[-1]
    nombre = "%s.%s" % (uuid_slug(uuid.uuid4()), extension)
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
                
# Señales
def borrar_portada(sender, instance, **kwargs):
    if instance.portada:
        try:
            os.remove(instance.portada.path)
        except OSError:
            pass   
        
pre_delete.connect(borrar_portada, sender=Evento)

