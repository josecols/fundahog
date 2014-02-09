#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from datetime import datetime
from django.utils import simplejson
from django.db.models.query_utils import Q
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from portal.forms import EventoForm, ImagenForm, CategoriaForm, \
    LibroForm, SeccionForm, ProgramaForm
from portal.models import Evento, Seccion, Organizacion, Galeria, \
    Album, Imagen, Libro, Categoria, Programa

ELEMENTOS_PAGINA = 10


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
    if isinstance(datos, QuerySet):
        datos = [model_to_dict(obj) for obj in datos]
    data['data'] = datos
    return simplejson.dumps(data)


def informacion_organizacion():
    try:
        organizacion = Organizacion.objects.all()[0]
        telefonos = organizacion.telefonos.filter(principal=True)
    except IndexError:
        return (None, None)
    return (organizacion.direccion, telefonos)


def eventos(request, pagina='1'):
    lista = Evento.objects.order_by('fecha').reverse()
    eventos = paginar(lista, pagina, ELEMENTOS_PAGINA)
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


def programas(request, pagina='1'):
    lista = Programa.objects.all()
    programas = paginar(lista, pagina, ELEMENTOS_PAGINA)
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('programas.html', {
        'programas': programas,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def programa(request, slug, programa_id):
    programa = get_object_or_404(Programa, pk=programa_id)
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('programa.html', {
        'programa': programa,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def nosotros(request, slug=None):
    seccion = get_object_or_404(Seccion, titulo='Nosotros')
    (direccion, telefonos) = informacion_organizacion()

    try:
        subseccion = Seccion.objects.get(slug=slug)
    except Seccion.DoesNotExist:
        subseccion = None

    return render_to_response('nosotros.html', {
        'seccion': seccion,
        'subseccion': subseccion,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def seccion(request, slug):
    seccion = get_object_or_404(Seccion, slug=slug)
    (direccion, telefonos) = informacion_organizacion()

    return render_to_response('seccion.html', {
        'seccion': seccion,
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


def galeria(request, galeria_pk=None):
    if galeria_pk:
        galeria = get_object_or_404(Galeria, pk=galeria_pk)
    else:
        galeria = get_object_or_404(Galeria, titulo='Principal')
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('galeria.html', {
        'galeria': galeria,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def libros(request, pagina='1'):
    lista = Libro.objects.all()
    libros = paginar(lista, pagina, ELEMENTOS_PAGINA)
    categorias = Categoria.objects.all()
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('libros.html', {
        'libros': libros,
        'categorias': categorias,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def libro(request, slug, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    categorias = Categoria.objects.all()
    (direccion, telefonos) = informacion_organizacion()
    return render_to_response('libro.html', {
        'libro': libro,
        'categorias': categorias,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


def libros_busqueda(request, pagina='1', query=None):
    if not query:
        query = request.GET.get('q', '')
    if query:
        qset = Q(titulo__icontains=query) \
            | Q(categorias__slug__icontains=query) \
            | Q(descripcion__icontains=query)
        lista = Libro.objects.filter(qset).distinct()
        libros = paginar(lista, pagina, ELEMENTOS_PAGINA)
    else:
        libros = None
    categorias = Categoria.objects.all()
    (direccion, telefonos) = informacion_organizacion()

    return render_to_response('libros-busqueda.html', {
        'libros': libros,
        'query': query,
        'categorias': categorias,
        'direccion': direccion,
        'telefonos': telefonos,
        'request': request,
        }, context_instance=RequestContext(request))


# Vistas AJAX

@csrf_protect
def evento_agregar(request):
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


@csrf_protect
def evento_modificar(request):
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
def evento_borrar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        evento_id = request.POST.get('evento', None)
        evento = get_object_or_404(Evento, pk=evento_id)
        evento.delete()
        return HttpResponse(construir_data(0, 'Evento borrado con éxito'
                            ), mimetype='application/javascript')

    raise Http404


@csrf_protect
def imagen_agregar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        album = get_object_or_404(Album, pk=request.POST.get('album',
                                  None))
        form = ImagenForm(request.POST, request.FILES)

        if form.is_valid():
            album.imagenes.add(form.save())
            return HttpResponse(construir_data(0,
                                'Imagen agregada con éxito'),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404


@csrf_protect
def imagen_borrar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        imagen_id = request.POST.get('imagen', None)
        imagen = get_object_or_404(Imagen, pk=imagen_id)
        imagen.delete()
        return HttpResponse(construir_data(0, 'Imagen borrada con éxito'
                            ), mimetype='application/javascript')

    raise Http404


@csrf_protect
def libro_agregar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():

        form = LibroForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse(construir_data(0,
                                'Libro agregado con éxito'),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404


@csrf_protect
def libro_modificar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        libro_id = request.POST.get('libro', None)
        libro = get_object_or_404(Libro, pk=libro_id)
        libro.titulo = request.POST.get('titulo', None)
        libro.descripcion = request.POST.get('descripcion', None)

        try:
            libro.full_clean()
            libro.save()
            return HttpResponse(construir_data(0,
                                "Libro modificado con éxito"),
                                mimetype='application/javascript')
        except ValidationError, errors:
            return HttpResponse(construir_data(-1,
                                errors.message_dict),
                                mimetype='application/javascript')


@csrf_protect
def libro_borrar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        libro_id = request.POST.get('libro', None)
        libro = get_object_or_404(Libro, pk=libro_id)
        libro.delete()
        return HttpResponse(construir_data(0, 'Libro borrado con éxito'
                            ), mimetype='application/javascript')
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


@csrf_protect
def seccion_agregar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():

        try:
            superseccion = \
                Seccion.objects.get(pk=request.POST.get('superseccion',
                                    None))
        except Seccion.DoesNotExist:
            superseccion = None

        form = SeccionForm(request.POST)

        if form.is_valid():
            if superseccion:
                superseccion.secciones.add(form.save())
            else:
                form.save()
            return HttpResponse(construir_data(0,
                                'Sección agregada con éxito'),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404


@csrf_protect
def seccion_modificar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        seccion_id = request.POST.get('seccion', None)
        seccion = get_object_or_404(Seccion, pk=seccion_id)
        seccion.titulo = request.POST.get('titulo', None)
        seccion.contenido = request.POST.get('contenido', None)

        try:
            seccion.full_clean()
            seccion.save()
            return HttpResponse(construir_data(0,
                                "Sección modificada con éxito"),
                                mimetype='application/javascript')
        except ValidationError, errors:
            return HttpResponse(construir_data(-1,
                                errors.message_dict),
                                mimetype='application/javascript')


@csrf_protect
def seccion_borrar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        seccion_id = request.POST.get('seccion', None)
        seccion = get_object_or_404(Seccion, pk=seccion_id)
        seccion.delete()
        return HttpResponse(construir_data(0,
                            'Sección borrada con éxito'),
                            mimetype='application/javascript')
    raise Http404


@csrf_protect
def programa_agregar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():

        form = ProgramaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse(construir_data(0,
                                'Programa agregado con éxito'),
                                mimetype='application/javascript')
        else:
            return HttpResponse(construir_data(-1, form.errors),
                                mimetype='application/javascript')
    raise Http404


@csrf_protect
def programa_modificar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        programa_id = request.POST.get('programa', None)
        programa = get_object_or_404(Programa, pk=programa_id)
        programa.titulo = request.POST.get('titulo', None)
        programa.contenido = request.POST.get('contenido', None)

        try:
            programa.full_clean()
            programa.save()
            return HttpResponse(construir_data(0,
                                "Programa modificado con éxito"),
                                mimetype='application/javascript')
        except ValidationError, errors:
            return HttpResponse(construir_data(-1,
                                errors.message_dict),
                                mimetype='application/javascript')


@csrf_protect
def programa_borrar(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        programa_id = request.POST.get('programa', None)
        programa = get_object_or_404(Programa, pk=programa_id)
        programa.delete()
        return HttpResponse(construir_data(0,
                            'Programa borrado con éxito'),
                            mimetype='application/javascript')
    raise Http404


@csrf_protect
def galerias(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        galerias = Galeria.objects.all()
        return HttpResponse(construir_data(0,
                            'Galerias consultadas con éxito',
                            galerias), mimetype='application/javascript'
                            )
    raise Http404


@csrf_protect
def albumes(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        galeria = request.POST.get('galeria', None)
        albumes = Album.objects.filter(galeria=galeria)
        return HttpResponse(construir_data(0,
                            'Albumes consultadas con éxito', albumes),
                            mimetype='application/javascript')
    raise Http404


@csrf_protect
def imagenes(request):
    if request.user.is_superuser and request.method == 'POST' \
        and request.is_ajax():
        album = request.POST.get('album', None)
        imagenes = Imagen.objects.filter(album=album)
        data = [{
            'id': imagen.pk,
            'titulo': imagen.titulo,
            'imagen': imagen.imagen.url,
            'thumbnail': imagen.thumbnail,
            } for imagen in imagenes]

        return HttpResponse(construir_data(0,
                            'Imagenes consultadas con éxito', data),
                            mimetype='application/javascript')
    raise Http404
