#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from django.http import Http404
from ayuda.models import Seccion
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from portal.views import informacion_organizacion, entrada_importante


def ayuda(request, slug=None, seccion_id=None):
    if request.user.is_superuser:
        try:
            seccion = Seccion.objects.get(pk=seccion_id)
        except Seccion.DoesNotExist:
            seccion = None

        secciones = Seccion.objects.all()
        (rif, direccion, telefonos) = informacion_organizacion()

        return render_to_response('ayuda.html', {
            'seccion': seccion,
            'secciones': secciones,
            'rif': rif,
            'direccion': direccion,
            'telefonos': telefonos,
            'importante': entrada_importante(request),
            'request': request,
            }, context_instance=RequestContext(request))
    raise Http404


