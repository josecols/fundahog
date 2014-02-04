#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from datetime import datetime
from django.utils import simplejson
from portal.forms import EventoForm
from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from portal.models import Evento, Seccion, Organizacion
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginar(lista, pagina, cantidad):
    paginator = Paginator(lista, cantidad)
    try:
        entradas = paginator.page(pagina)
    except PageNotAnInteger:
        entradas = paginator.page(1)
    except EmptyPage:
        entradas = paginator.page(paginator.num_pages)
    return entradas


def construir_data(flag, msg, datos=None):
    data = {}
    if flag == 0:
        data['flag'] = 0
        data['msg'] = msg
    else:
        data['flag'] = -1
        data['errores'] = msg
    data['data'] = datos
    return simplejson.dumps(data)


def informacion_organizacion():
    organizacion = Organizacion.objects.all()[0]
    telefonos = organizacion.telefonos.filter(principal=True)
    return (organizacion.direccion, telefonos)


def eventos(request):
    eventos = Evento.objects.all()
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('eventos.html', {
        'eventos': eventos,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def evento(request, slug, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('evento.html', {
        'evento': evento,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def programas(request):
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('programas.html',
                              {'direccion': direccion,
                              'telefonos': telefonos,
                              'request': request},
                              context_instance=RequestContext(request))


def nosotros(request, slug=None):
    seccion = get_object_or_404(Seccion, titulo='Nosotros')
    (direccion, telefonos) = informacion_organizacion()

    if slug:
        subseccion = get_object_or_404(Seccion, slug=slug)
    else:
        subseccion = None

    return render_to_response('nosotros.html', {
        'seccion': seccion,
        'subseccion': subseccion,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def contacto(request):
    organizacion = Organizacion.objects.all()[0]
    telefonos_principales = \
        organizacion.telefonos.filter(principal=True)
    return render_to_response('contacto.html',
                              {'organizacion': organizacion,
                              'telefonos_principales': telefonos_principales,
                              'request': request},
                              context_instance=RequestContext(request))


def galeria(request):
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('galeria.html', {'direccion': direccion,
                              'telefonos': telefonos,
                              'request': request},
                              context_instance=RequestContext(request))


def libros(request):
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('libros.html', {'direccion': direccion,
                              'telefonos': telefonos,
                              'request': request},
                              context_instance=RequestContext(request))


# Vistas AJAX

@csrf_protect
def modificar_evento(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        evento_id = request.POST.get('evento', None)
        evento = get_object_or_404(Evento, pk=evento_id)
        evento.titulo = request.POST.get('titulo', None)
        evento.contenido = request.POST.get('contenido', None)

        try:
            evento.full_clean()
            evento.save()
            return HttpResponse(construir_data(0,
                                "Evento modificado con éxito"),
                                mimetype='application/javascript')
        except ValidationError, errors:
            return HttpResponse(construir_data(-1,
                                errors.message_dict),
                                mimetype='application/javascript')

    raise Http404


@csrf_protect
def borrar_evento(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        evento_id = request.POST.get('evento', None)
        evento = get_object_or_404(Evento, pk=evento_id)
        evento.delete()
        return HttpResponse(construir_data(0, 'Evento borrado con éxito'
                            ), mimetype='application/javascript')

    raise Http404


@csrf_protect
def agregar_evento(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        post = request.POST.copy()
        post['fecha'] = datetime.strptime(post['fecha'],
                '%d-%m-%Y %H:%M')
        form = EventoForm(post, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse(construir_data(0,
                                'Evento agregado con éxito'),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404

