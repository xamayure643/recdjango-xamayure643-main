from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Plataforma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    CALIFICACIONES_EDAD = [
        ('PEGI3', 'PEGI 3'),
        ('PEGI7', 'PEGI 7'),
        ('PEGI12', 'PEGI 12'),
        ('PEGI16', 'PEGI 16'),
        ('PEGI18', 'PEGI 18'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    pegi = models.CharField(max_length=10, choices=CALIFICACIONES_EDAD, default='PEGI3')
    fecha_lanzamiento = models.DateField()

    categorias = models.ManyToManyField(Categoria, related_name='juegos')
    plataformas = models.ManyToManyField(Plataforma, related_name='juegos')

    def __str__(self):
        return self.nombre

class EstadoJuego(models.Model):
    OPCIONES_ESTADO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_CURSO', 'En curso'),
        ('COMPLETADO', 'Completado'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_listas')

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='en_listas_usuarios')

    estado = models.CharField(max_length=15, choices=OPCIONES_ESTADO)
    es_favorito = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'juego')

    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre} ({self.estado})"


class Opinion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mis_opiniones')

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='opiniones')
    
    texto_opinion = models.TextField(blank=True, null=True)
    plataforma_jugado = models.ForeignKey(Plataforma, on_delete=models.SET_NULL, null=True)
    compartir_en_comentarios = models.BooleanField(default=False)
    
    nota_gameplay = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    nota_sonido = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    nota_banda_sonora = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    nota_historia = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"Opinión de {self.usuario.username} sobre {self.juego.nombre}"

    @property
    def nota_general(self):
        return (self.nota_gameplay + self.nota_sonido + self.nota_banda_sonora + self.nota_historia) / 4