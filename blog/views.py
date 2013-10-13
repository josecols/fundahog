# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols
from blog.models import Entrada
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, render_to_response

def index(request):
    entradas = Entrada.objects.all()
    return render_to_response('blog.html',
                              {'entradas':entradas, 'request':request},
                              context_instance=RequestContext(request))

def entrada(request, slug, entrada_id):
    entrada = get_object_or_404(Entrada, pk=entrada_id)
    return render_to_response('entrada.html',
                              {'entrada':entrada, 'request':request},
                              context_instance=RequestContext(request))

# Vistas AJAX
@csrf_protect
def modificar(request):
    if request.user.is_superuser and request.method == 'POST':        
        entrada_id = request.POST.get('entrada', None)
        entrada = get_object_or_404(Entrada, pk=entrada_id)         
        titulo = request.POST.get('titulo', None)
        contenido = request.POST.get('contenido', None)
        
        if (titulo and contenido):
            entrada.titulo = titulo
            entrada.contenido = contenido
            entrada.save()
            return HttpResponse(simplejson.dumps("Entrada modificada con éxito"), mimetype='application/javascript')
    raise Http404
