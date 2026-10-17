from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    numero_pedido = models.CharField(max_length=20, unique=True)
    cliente = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=500)
    valor_total = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'Pedido {self.numero_pedido} - {self.cliente}'