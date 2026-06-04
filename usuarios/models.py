from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    OPCIONES_PRIVACIDAD = [
        ('TODOS', 'Todos'),
        ('NADIE', 'Nadie'),
        ('AMIGOS', 'Solo Amigos'),
    ]
    
    foto_perfil = models.URLField(max_length=500, blank=True, null=True, default="https://via.placeholder.com/150")
    privacidad = models.CharField(max_length=10, choices=OPCIONES_PRIVACIDAD, default='TODOS')

    def __str__(self):
        return self.username

class Relacion(models.Model):
    usuario_origen = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='siguiendo')
    usuario_destino = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguidores')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario_origen', 'usuario_destino')

    def __str__(self):
        return f"{self.usuario_origen} sigue a {self.usuario_destino}"