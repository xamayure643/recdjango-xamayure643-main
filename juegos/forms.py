from django import forms
from .models import Juego, Opinion

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'descripcion', 'pegi', 'fecha_lanzamiento', 'categorias', 'plataformas']
        widgets = {
            'fecha_lanzamiento': forms.DateInput(attrs={'type': 'date'}),
            'categorias': forms.CheckboxSelectMultiple(), 
            'plataformas': forms.CheckboxSelectMultiple(),
        }

class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['texto_opinion', 'nota_gameplay', 'nota_sonido', 'nota_banda_sonora', 'nota_historia']