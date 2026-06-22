from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import NumeroLoteria
from .forms import NumeroLoteriaForm


def registrar_numero(request):
    """CU-01: Registrar Numero de Loteria"""
    if request.method == 'POST':
        form = NumeroLoteriaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Numero registrado exitosamente.")
                return redirect('loteria:listar')
            except Exception:
                messages.error(request, "Error al guardar el registro.")
    else:
        form = NumeroLoteriaForm()

    return render(request, 'loteria/registrar.html', {'form': form})


def listar_numeros(request):
    """CU-04: Listar Numeros de Loteria"""
    fecha_filtro = request.GET.get('fecha', '')
    if fecha_filtro:
        numeros = NumeroLoteria.objects.filter(fecha=fecha_filtro)
    else:
        numeros = NumeroLoteria.objects.all()

    return render(request, 'loteria/listar.html', {
        'numeros': numeros,
        'fecha_filtro': fecha_filtro,
    })


def actualizar_numero(request, pk):
    """CU-02: Actualizar Numero de Loteria"""
    numero_obj = get_object_or_404(NumeroLoteria, pk=pk)

    # Validar que la fecha de sorteo no haya pasado (FE-01)
    if numero_obj.fecha < date.today():
        messages.error(
            request,
            "No se permite modificar: la fecha de sorteo ya paso."
        )
        return redirect('loteria:listar')

    if request.method == 'POST':
        form = NumeroLoteriaForm(request.POST, instance=numero_obj)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Numero actualizado exitosamente.")
                return redirect('loteria:listar')
            except Exception:
                messages.error(request, "Error al actualizar el registro.")
    else:
        form = NumeroLoteriaForm(instance=numero_obj)

    return render(request, 'loteria/actualizar.html', {
        'form': form,
        'numero_obj': numero_obj,
    })


def eliminar_numero(request, pk):
    """CU-03: Eliminar Numero de Loteria"""
    numero_obj = get_object_or_404(NumeroLoteria, pk=pk)

    # Validar que la fecha de sorteo no haya pasado (FE-01)
    if numero_obj.fecha < date.today():
        messages.error(
            request,
            "No se permite eliminar: la fecha de sorteo ya paso."
        )
        return redirect('loteria:listar')

    if request.method == 'POST':
        try:
            numero_obj.delete()
            messages.success(request, "Numero eliminado exitosamente.")
            return redirect('loteria:listar')
        except Exception:
            messages.error(request, "Error al eliminar el registro.")

    return render(request, 'loteria/eliminar.html', {
        'numero_obj': numero_obj,
    })
