from datetime import date
from django import forms
from .models import NumeroLoteria


class NumeroLoteriaForm(forms.ModelForm):

    class Meta:
        model = NumeroLoteria
        fields = ['numero', 'propietario', 'fecha']
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 4521',
                'min': '0',
                'max': '9999',
            }),
            'propietario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del comprador',
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if numero < 0 or numero > 9999:
            raise forms.ValidationError(
                "El numero debe ser exactamente de 4 cifras (0000-9999)."
            )
        return numero

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < date.today():
            raise forms.ValidationError(
                "No se permite registrar numeros para sorteos cuya fecha ya paso."
            )
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get('numero')
        fecha = cleaned_data.get('fecha')

        if numero is not None and fecha:
            qs = NumeroLoteria.objects.filter(numero=numero, fecha=fecha)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "Numero duplicado: este numero ya esta registrado para esa fecha de sorteo."
                )

        return cleaned_data
