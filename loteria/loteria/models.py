from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class NumeroLoteria(models.Model):

    numero = models.PositiveIntegerField(
        verbose_name="Numero de Loteria",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999),
        ]
    )

    propietario = models.CharField(
        max_length=150,
        verbose_name="Nombre del Propietario"
    )

    fecha = models.DateField(
        verbose_name="Fecha del Sorteo"
    )

    class Meta:
        verbose_name = "Numero de Loteria"
        verbose_name_plural = "Numeros de Loteria"
        unique_together = ['numero', 'fecha']

    def __str__(self):
        return f"{self.numero:04d} - {self.propietario} ({self.fecha})"
