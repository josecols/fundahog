#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from ayuda.models import Seccion


class SeccionForm(forms.ModelForm):

    class Meta:

        model = Seccion


