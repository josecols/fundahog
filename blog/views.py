#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from blog.models import Categoria, Entrada
from django.db.models.query_utils import Q
from django.http import Http404, HttpResponse
from blog.forms import EntradaForm, CategoriaForm
from django.template.context import RequestContext
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, render_to_response
from portal.views import construir_data, paginar, \
    informacion_organizacion, entrada_importante

ENTRADAS = 10  # Publicaciones por página


def index(request, pagina='1'):
    lista = Entrada.objects.order_by('creado').reverse()
    entradas = paginar(lista, pagina, ENTRADAS)
    categorias = Categoria.objects.all()
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('blog.html', {
        'entradas': entradas,
        'categorias': categorias,
        'direccion': direccion,
        'telefonos': telefonos,
        'importante': entrada_importante(request),
        'request': request,
        }, context_instance=RequestContext(request))


def entrada(request, slug, entrada_id):
    entrada = get_object_or_404(Entrada, pk=entrada_id)
    categorias = Categoria.objects.all()
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('entrada.html', {
        'entrada': entrada,
        'categorias': categorias,
        'direccion': direccion,
        'telefonos': telefonos,
        'importante': entrada_importante(request),
        'request': request,
        }, context_instance=RequestContext(request))


def busqueda(request, pagina='1', query=None):
    if not query:
        query = request.GET.get('q', '')
    if query:
        qset = Q(titulo__icontains=query) \
            | Q(categorias__slug__icontains=query) \
            | Q(contenido__icontains=query)
        lista = Entrada.objects.filter(qset).distinct()
        lista = lista.order_by('creado').reverse()
        entradas = paginar(lista, pagina, ENTRADAS * 2)
    else:
        entradas = None
    categorias = Categoria.objects.all()
    (direccion, telefonos) = informacion_organizacion()

    return render_to_response('blog-busqueda.html', {
        'entradas': entradas,
        'query': query,
        'categorias': categorias,
        'direccion': direccion,
        'telefonos': telefonos,
        'importante': entrada_importante(request),
        'request': request,
        }, context_instance=RequestContext(request))


# Vistas AJAX

@csrf_protect
def entrada_agregar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        titulo = request.POST.get('titulo', None)
        contenido = request.POST.get('contenido', None)
        categorias = str(request.POST.get('categorias', None)).split(','
                )
        importante = request.POST.get('importante', None) == 'True'

        form = EntradaForm(request.POST)

        if form.is_valid():
            entrada = Entrada(titulo=titulo, contenido=contenido,
                              importante=importante, autor=request.user)
            entrada.save()
            for pk in categorias:
                categoria = Categoria.objects.get(pk=pk)
                entrada.categorias.add(categoria)
            return HttpResponse(construir_data(0,
                                "Entrada agregada con éxito"),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404


@csrf_protect
def entrada_modificar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        entrada_id = request.POST.get('entrada', None)
        entrada = get_object_or_404(Entrada, pk=entrada_id)
        entrada.titulo = request.POST.get('titulo', None)
        entrada.contenido = request.POST.get('contenido', None)
        entrada.importante = request.POST.get('importante', None)

        try:
            entrada.full_clean()
            entrada.save()
            return HttpResponse(construir_data(0,
                                "Entrada modificada con éxito"),
                                mimetype='application/javascript')
        except ValidationError, errors:
            return HttpResponse(construir_data(-1,
                                errors.message_dict),
                                mimetype='application/javascript')

    raise Http404


@csrf_protect
def entrada_borrar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        entrada_id = request.POST.get('entrada', None)
        entrada = get_object_or_404(Entrada, pk=entrada_id)
        entrada.delete()
        return HttpResponse(construir_data(0,
                            "Entrada borrada con éxito"),
                            mimetype='application/javascript')

    raise Http404


@csrf_protect
def categoria_agregar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        descripcion = request.POST.get('descripcion', None)

        form = CategoriaForm(request.POST)

        if form.is_valid():
            categoria = Categoria(descripcion=descripcion)
            categoria.save()
            return HttpResponse(construir_data(0,
                                "Categoría agregada con éxito",
                                str(categoria.pk)),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404
