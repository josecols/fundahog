# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463
from datetime import datetime
from portal.models import Evento
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import  render_to_response, get_object_or_404

def eventos(request):
    eventos = Evento.objects.all()
    return render_to_response('eventos.html',
                              {'eventos':eventos, 'request':request},
                              context_instance=RequestContext(request))


def evento(request, slug, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return render_to_response('evento.html',
                              {'evento':evento, 'request':request},
                              context_instance=RequestContext(request))

def programas(request):
    return render_to_response('programas.html', {'request':request}, context_instance=RequestContext(request))

def nosotros(request):
    return render_to_response('nosotros.html', {'request':request}, context_instance=RequestContext(request))

def contacto(request):
    return render_to_response('contacto.html', {'request':request}, context_instance=RequestContext(request))

def galeria(request):
    return render_to_response('galeria.html', {'request':request}, context_instance=RequestContext(request))

def libros(request):
    return render_to_response('libros.html', {'request':request}, context_instance=RequestContext(request))

# Vistas AJAX
@csrf_protect
def modificar_evento(request):
    if request.user.is_superuser and request.method == 'POST' and request.is_ajax():
        evento_id = request.POST.get('evento', None)
        evento = get_object_or_404(Evento, pk=evento_id)         
        titulo = request.POST.get('titulo', None)
        contenido = request.POST.get('contenido', None)
        
        if (titulo and contenido):
            evento.titulo = titulo
            evento.contenido = contenido
            evento.save()
            return HttpResponse(simplejson.dumps("Evento modificado con éxito"), mimetype='application/javascript')
    raise Http404

@csrf_protect
def borrar_evento(request):
    if request.user.is_superuser and request.method == 'POST' and request.is_ajax():
        evento_id = request.POST.get('evento', None)
        evento = get_object_or_404(Evento, pk=evento_id)
        evento.delete()
        return HttpResponse(simplejson.dumps("Evento borrado con éxito"), mimetype='application/javascript')
                
    raise Http404

@csrf_protect
def agregar_evento(request):
    if request.user.is_superuser and request.method == 'POST' and request.is_ajax():
        titulo = request.POST.get('titulo', None)
        contenido = request.POST.get('contenido', None)
        fecha = request.POST.get('fecha', None)                
        fecha = datetime.strptime(fecha, '%d-%m-%Y %H:%M')
        
        if (titulo and contenido and fecha):
            evento = Evento(titulo=titulo, contenido=contenido, fecha=fecha)
            evento.save()            
            return HttpResponse(simplejson.dumps("Evento agregado con éxito"), mimetype='application/javascript')
    raise Http404
