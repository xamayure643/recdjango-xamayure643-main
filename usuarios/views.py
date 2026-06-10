from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator  # <-- ¡Importante para paginar a mano!

from .forms import RegistroForm, PerfilForm
from .models import Usuario, Relacion
from juegos.models import EstadoJuego

class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    
    def get_success_url(self):
        return reverse_lazy('usuarios:login')
    
class PerfilDetailView(DetailView):
    model = Usuario
    template_name = 'usuarios/perfil_detalle.html'
    context_object_name = 'perfil_usuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil_usuario = self.object # El usuario al que estamos visitando
        visitante = self.request.user # El usuario que está navegando en la web

        puede_ver = False
        lo_sigue = False
        son_amigos = False

        # COMPROBAR SEGUIMIENTOS (Usa usuario_origen y usuario_destino de tu modelo Relacion)
        if visitante.is_authenticated and visitante != perfil_usuario:
            lo_sigue = Relacion.objects.filter(usuario_origen=visitante, usuario_destino=perfil_usuario).exists()
            lo_siguen = Relacion.objects.filter(usuario_origen=perfil_usuario, usuario_destino=visitante).exists()
            
            if lo_sigue and lo_siguen:
                son_amigos = True

        context['lo_sigue'] = lo_sigue
        context['son_amigos'] = son_amigos

        # LÓGICA DE PRIVACIDAD
        if visitante == perfil_usuario:
            puede_ver = True # Uno mismo siempre puede ver su perfil
        elif perfil_usuario.privacidad == 'TODOS':
            puede_ver = True # Es público
        elif perfil_usuario.privacidad == 'AMIGOS':
            puede_ver = son_amigos # Seguimiento mutuo necesario
        elif perfil_usuario.privacidad == 'NADIE':
            puede_ver = False # Nadie salvo él mismo

        context['puede_ver'] = puede_ver

        # NUEVO APARTADO: FILTRADO Y PAGINACIÓN SI TIENE PERMISO
        if puede_ver:
            # 1. Obtenemos el QuerySet base de los juegos de este perfil
            juegos_queryset = EstadoJuego.objects.filter(usuario=perfil_usuario)
            
            # 2. Filtramos según el parámetro 'estado' de la URL
            estado = self.request.GET.get('estado')
            if estado in ['PENDIENTE', 'EN_CURSO', 'COMPLETADO']:
                juegos_queryset = juegos_queryset.filter(estado=estado)
            
            # 3. Guardamos el estado en el contexto para pintar los botones
            context['estado_actual'] = estado if estado else 'TODO'
            
            # 4. Paginamos manualmente de 5 en 5 elementos
            paginator = Paginator(juegos_queryset, 5)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            # 5. Pasamos el objeto de página al contexto (contiene los juegos de la página actual)
            context['page_obj'] = page_obj

        return context

# VISTA PARA EDITAR EL PERFIL
class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = PerfilForm
    template_name = 'usuarios/perfil_editar.html'
    
    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('usuarios:perfil_detalle', kwargs={'pk': self.request.user.pk})

# ACCIÓN SEGUIR / DEJAR DE SEGUIR
@login_required
def toggle_seguir(request, pk):
    usuario_a_seguir = get_object_or_404(Usuario, pk=pk)
    visitante = request.user

    if visitante != usuario_a_seguir:
        relacion = Relacion.objects.filter(usuario_origen=visitante, usuario_destino=usuario_a_seguir).first()
        
        if relacion:
            relacion.delete()
        else:
            Relacion.objects.create(usuario_origen=visitante, usuario_destino=usuario_a_seguir)

    return redirect('usuarios:perfil_detalle', pk=pk)