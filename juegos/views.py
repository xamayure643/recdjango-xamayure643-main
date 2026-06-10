from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Juego, Opinion, EstadoJuego, Categoria, Plataforma
from .forms import JuegoForm, OpinionForm, CategoriaFormSet, PlataformaFormSet

@login_required
def cambiar_estado(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        opciones = ['PENDIENTE', 'EN_CURSO', 'COMPLETADO']
        
        if nuevo_estado in opciones:
            estado_obj, _ = EstadoJuego.objects.get_or_create(usuario=request.user, juego=juego)
            estado_obj.estado = nuevo_estado
            estado_obj.save()
            
        elif nuevo_estado == 'ELIMINAR':
            EstadoJuego.objects.filter(usuario=request.user, juego=juego).delete()
            
    return redirect('juegos:detalle', pk=pk)

class JuegoListView(ListView):
    model = Juego
    template_name = 'juegos/lista.html'
    context_object_name = 'juegos'
    paginate_by = 10

class JuegoDetailView(DetailView):
    model = Juego
    template_name = 'juegos/detalle.html'
    context_object_name = 'juego'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            opinion = Opinion.objects.filter(usuario=self.request.user, juego=self.object).first()
            context['mi_opinion'] = opinion
            context['opinion_form'] = OpinionForm(instance=opinion)

            estado_actual = EstadoJuego.objects.filter(usuario=self.request.user, juego=self.object).first()
            context['mi_estado'] = estado_actual
            
        return context

class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class GestionarCategoriasView(SoloAdminMixin, View):
    template_name = 'juegos/gestionar_extras.html'

    def get(self, request):
        formset = CategoriaFormSet(queryset=Categoria.objects.none())
        return render(request, self.template_name, {'formset': formset, 'titulo': 'Añadir Categorías Múltiples'})

    def post(self, request):
        formset = CategoriaFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('juegos:lista')
        return render(request, self.template_name, {'formset': formset, 'titulo': 'Añadir Categorías Múltiples'})

class GestionarPlataformasView(SoloAdminMixin, View):
    template_name = 'juegos/gestionar_extras.html'

    def get(self, request):
        formset = PlataformaFormSet(queryset=Plataforma.objects.none())
        return render(request, self.template_name, {'formset': formset, 'titulo': 'Añadir Plataformas Múltiples'})

    def post(self, request):
        formset = PlataformaFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('juegos:lista')
        return render(request, self.template_name, {'formset': formset, 'titulo': 'Añadir Plataformas Múltiples'})

class JuegoCreateView(SoloAdminMixin, CreateView):
    model = Juego
    form_class = JuegoForm
    template_name = 'juegos/crear_editar.html'
    success_url = reverse_lazy('juegos:lista')

class JuegoUpdateView(SoloAdminMixin, UpdateView):
    model = Juego
    form_class = JuegoForm
    template_name = 'juegos/crear_editar.html'
    success_url = reverse_lazy('juegos:lista')

class JuegoDeleteView(SoloAdminMixin, DeleteView):
    model = Juego
    template_name = 'juegos/confirmar_borrado.html'
    success_url = reverse_lazy('juegos:lista')

@login_required
def guardar_opinion(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    
    opinion, _ = Opinion.objects.get_or_create(usuario=request.user, juego=juego)
    
    if request.method == 'POST':
        form = OpinionForm(request.POST, instance=opinion)
        if form.is_valid():
            info_opinion = form.save(commit=False)
            
            if 'compartir' in request.POST:
                info_opinion.compartir_en_comentarios = True
            elif 'privar' in request.POST:
                info_opinion.compartir_en_comentarios = False
                
            info_opinion.save()
            return redirect('juegos:detalle', pk=juego.pk)
        
class MisJuegosView(LoginRequiredMixin, ListView):
    model = EstadoJuego
    template_name = 'juegos/mis_juegos.html'
    context_object_name = 'mis_estados'
    paginate_by = 10

    def get_queryset(self):
        queryset = EstadoJuego.objects.filter(usuario=self.request.user)
        
        estado = self.request.GET.get('estado')
        if estado in ['PENDIENTE', 'EN_CURSO', 'COMPLETADO']:
            queryset = queryset.filter(estado=estado)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estado_actual'] = self.request.GET.get('estado', 'TODO')
        return context