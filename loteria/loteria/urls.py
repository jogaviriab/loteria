from django.urls import path
from . import views

app_name = 'loteria'

urlpatterns = [
    path('registrar/', views.registrar_numero, name='registrar'),
    path('listar/', views.listar_numeros, name='listar'),
    path('actualizar/<int:pk>/', views.actualizar_numero, name='actualizar'),
    path('eliminar/<int:pk>/', views.eliminar_numero, name='eliminar'),
]
