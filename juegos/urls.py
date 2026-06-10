from django.urls import path
from . import views

app_name = 'juegos'

urlpatterns = [
    path('', views.JuegoListView.as_view(), name='lista'), 
    path('mis-juegos/', views.MisJuegosView.as_view(), name='mis_juegos'),
    path('<int:pk>/', views.JuegoDetailView.as_view(), name='detalle'),
    path('crear/', views.JuegoCreateView.as_view(), name='crear'),
    path('<int:pk>/editar/', views.JuegoUpdateView.as_view(), name='editar'), 
    path('<int:pk>/eliminar/', views.JuegoDeleteView.as_view(), name='eliminar'),
    path('<int:pk>/opinion/', views.guardar_opinion, name='guardar_opinion'),
    path('<int:pk>/cambiar-estado/', views.cambiar_estado, name='cambiar_estado'),
    path('categorias/añadir/', views.GestionarCategoriasView.as_view(), name='gestionar_categorias'),
    path('plataformas/añadir/', views.GestionarPlataformasView.as_view(), name='gestionar_plataformas'),
]