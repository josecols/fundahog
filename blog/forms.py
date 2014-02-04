#!/usr/bin/python
# -*- coding: utf-8 -*-

# FUNDAHOG - Django 1.4 - Python 2.7.3
# Universidad Católica Andrés Bello Guayana
# Desarrollado por José Cols - josecolsg@gmail.com - @josecols - (0414)8530463

from django import forms
from blog.models import Entrada, Categoria


class EntradaForm(forms.ModelForm):

    class Meta:

        model = Entrada


class CategoriaForm(forms.ModelForm):

    class Meta:

        model = Categoria


