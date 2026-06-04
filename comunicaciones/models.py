from django.db import models
from django.conf import settings
from juegos.models import Juego
from django.core.exceptions import ValidationError

class PeticionCreacion(models.Model):
    OPCIONES_ESTADO = [
        ('PENDIENTE', 'Pendiente'),
        ('CUMPLIDA', 'Cumplida'),
        ('RECHAZADA', 'Rechazada'),
    ]
    OPCIONES_PEGI = [
        ('PEGI3', 'PEGI 3'),
        ('PEGI7', 'PEGI 7'),
        ('PEGI12', 'PEGI 12'),
        ('PEGI16', 'PEGI 16'),
        ('PEGI18', 'PEGI 18'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_peticiones_creacion')
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    pegi = models.CharField(max_length=10, choices=OPCIONES_PEGI, default='PEGI3')
    fecha_lanzamiento = models.DateField()
    categorias = models.CharField(max_length=255)
    plataformas = models.CharField(max_length=255)
    mensaje_usuario = models.TextField(blank=True, null=True)
    fecha_peticion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=OPCIONES_ESTADO, default='PENDIENTE')
    motivo_rechazo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Crear: {self.nombre} - Estado: {self.estado}"
    
    def clean(self):
        if self.estado == 'RECHAZADA' and not self.motivo_rechazo:
            raise ValidationError("Debes proporcionar un motivo de rechazo si la petición es rechazada.")
        
        if self.estado != 'RECHAZADA':
            self.motivo_rechazo = None


class SugerenciaCambio(models.Model):
    OPCIONES_ESTADO = [
        ('PENDIENTE', 'Pendiente'),
        ('CUMPLIDA', 'Cumplida'),
        ('RECHAZADA', 'Rechazada'),
    ]
    OPCIONES_PEGI = [
        ('PEGI3', 'PEGI 3'),
        ('PEGI7', 'PEGI 7'),
        ('PEGI12', 'PEGI 12'),
        ('PEGI16', 'PEGI 16'),
        ('PEGI18', 'PEGI 18'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_sugerencias_cambio')

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='sugerencias_cambio')
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    pegi = models.CharField(max_length=10, choices=OPCIONES_PEGI, default='PEGI3')
    fecha_lanzamiento = models.DateField()
    categorias = models.CharField(max_length=255)
    plataformas = models.CharField(max_length=255)
    mensaje_usuario = models.TextField(blank=True, null=True)
    fecha_sugerencia = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=OPCIONES_ESTADO, default='PENDIENTE')
    motivo_rechazo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cambio en: {self.juego.nombre} - Estado: {self.estado}"
    
    def clean(self):
        if self.estado == 'RECHAZADA' and not self.motivo_rechazo:
            raise ValidationError("Debes proporcionar un motivo de rechazo si la petición es rechazada.")
        
        if self.estado != 'RECHAZADA':
            self.motivo_rechazo = None


class Notificacion(models.Model):
    usuario_destino = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')

    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Para {self.usuario_destino.username} - Leído: {self.leido}"