from django import forms
from portal.models import Evento, Seccion
from django.core.files.images import get_image_dimensions

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        
    def clean_portada(self):
        imagen = self.cleaned_data.get("portada")
        if imagen:
            ancho, alto = get_image_dimensions(imagen)
            if ancho <= 200 and alto <= 200:
                raise forms.ValidationError("La imagen debe tener un ancho y un alto mayor a 200px")
        return imagen                
    
    
class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        
    def __init__(self, *args, **kwargs):
        super(SeccionForm, self).__init__(*args, **kwargs)
        self.fields['secciones'].queryset = Seccion.objects.exclude(id__exact=self.instance.pk)     
