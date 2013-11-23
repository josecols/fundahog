# encoding:utf-8
# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463
from blog.models import Categoria, Entrada
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q


# Publicaciones por página
ENTRADAS = 10

def paginar(lista, pagina, cantidad):
    paginator = Paginator(lista, cantidad)    
    try:
        entradas = paginator.page(pagina)
    except PageNotAnInteger:
        entradas = paginator.page(1)
    except EmptyPage:
        entradas = paginator.page(paginator.num_pages)     
    return entradas


def index(request, pagina='1'):    
    lista = Entrada.objects.order_by('creado').reverse()
    entradas = paginar(lista, pagina, ENTRADAS)      
    categorias = Categoria.objects.all()
    return render_to_response('blog.html',
                              {'entradas':entradas, 'categorias':categorias, 'request':request},
                              context_instance=RequestContext(request))


def entrada(request, slug, entrada_id):
    entrada = get_object_or_404(Entrada, pk=entrada_id)
    categorias = Categoria.objects.all()
    return render_to_response('entrada.html',
                              {'entrada':entrada, 'categorias':categorias, 'request':request},
                              context_instance=RequestContext(request))


def busqueda(request, pagina="1", query=None):
    if not query:
        query = request.GET.get('q', '')
    if query:
        qset = (Q(titulo__icontains=query) | Q(categorias__descripcion__icontains=query) | Q(contenido__icontains=query))
        lista = Entrada.objects.filter(qset).distinct()
        entradas = paginar(lista, pagina, ENTRADAS * 2)
    else:
        entradas = None
    categorias = Categoria.objects.all()
            
    return render_to_response('busqueda.html',
                              {'entradas': entradas, 'query': query, 'categorias':categorias, 'request':request},
                              context_instance=RequestContext(request))
# Vistas AJAX
@csrf_protect
def agregar(request):
    if request.user.is_superuser and request.method == 'POST':                
        titulo = request.POST.get('titulo', None)
        contenido = request.POST.get('contenido', None)
        categorias = str(request.POST.get('categorias', None)).split(',')
        
        if (titulo and contenido and categorias):
            entrada = Entrada(titulo=titulo, contenido=contenido, autor=request.user)
            entrada.save()            
            for pk in categorias:
                categoria = Categoria.objects.get(pk=pk)
                entrada.categorias.add(categoria)
            return HttpResponse(simplejson.dumps("Entrada agregada con éxito"), mimetype='application/javascript')
    raise Http404

@csrf_protect
def agregar_categoria(request):
    if request.user.is_superuser and request.method == 'POST':
        descripcion = request.POST.get('descripcion', None)
        
        if (descripcion):
            categoria = Categoria(descripcion=descripcion)
            categoria.save()
            return HttpResponse(simplejson.dumps(str(categoria.pk)), mimetype='application/javascript')
    raise Http404
        

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

@csrf_protect
def borrar(request):
    if request.user.is_superuser and request.method == 'POST':        
        entrada_id = request.POST.get('entrada', None)
        entrada = get_object_or_404(Entrada, pk=entrada_id)
        entrada.delete()
        return HttpResponse(simplejson.dumps("Entrada borrada con éxito"), mimetype='application/javascript')
                
    raise Http404
