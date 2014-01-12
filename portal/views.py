# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463
from datetime import datetime
from portal.models import Evento
from django.utils import simplejson
from portal.forms import EventoForm
from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import  render_to_response, get_object_or_404

def construir_data(flag, msg):
    data = {}
    if (flag == 0):
        data['flag'] = 0
        data['msg'] = msg
    else:
        data['flag'] = -1
        data['errores'] = msg
        
    return simplejson.dumps(data)

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
        evento.titulo = request.POST.get('titulo', None)
        evento.contenido = request.POST.get('contenido', None)        
        
        try:
            evento.full_clean()
            evento.save()
            return HttpResponse(construir_data(0, "Evento modificado con éxito"), mimetype='application/javascript')
        except ValidationError as errors:        
            return HttpResponse(construir_data(-1, errors.message_dict), mimetype='application/javascript') 
            
    raise Http404

@csrf_protect
def borrar_evento(request):
    if request.user.is_superuser and request.method == 'POST' and request.is_ajax():
        evento_id = request.POST.get('evento', None)
        evento = get_object_or_404(Evento, pk=evento_id)
        evento.delete()
        return HttpResponse(construir_data(0, 'Evento borrado con éxito'), mimetype='application/javascript')
                
    raise Http404

@csrf_protect
def agregar_evento(request):
    if request.user.is_superuser and request.method == 'POST' and request.is_ajax():      
        post = request.POST.copy()
        post['fecha'] = datetime.strptime(post['fecha'], '%d-%m-%Y %H:%M')              
        form = EventoForm(post, request.FILES)
        
        if (form.is_valid()):
            form.save()      
            return HttpResponse(construir_data(0, 'Evento agregado con éxito'), mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors), mimetype='application/javascript')
    raise Http404

