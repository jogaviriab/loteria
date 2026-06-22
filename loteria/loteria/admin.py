from django.contrib import admin
from .models import NumeroLoteria


@admin.register(NumeroLoteria)
class NumeroLoteriaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'propietario', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('numero', 'propietario')
