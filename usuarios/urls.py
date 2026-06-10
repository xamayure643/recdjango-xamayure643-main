from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('perfil/editar/', views.PerfilUpdateView.as_view(), name='perfil_editar'),
    path('perfil/<int:pk>/', views.PerfilDetailView.as_view(), name='perfil_detalle'),
    path('perfil/<int:pk>/seguir/', views.alternar_seguir, name='alternar_seguir'),
]