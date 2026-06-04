from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroForm

class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    
    def get_success_url(self):
        return reverse_lazy('usuarios:login')