from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("username", "email")

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Elegimos los campos que el usuario podrá editar
        fields = ['username', 'foto_perfil', 'privacidad']