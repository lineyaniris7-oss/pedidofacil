from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'cliente', 'descripcion', 'valor_total', 'estado']
        labels = {
            'numero_pedido': 'Número de pedido',
            'cliente': 'Nombre del cliente',
            'descripcion': 'Descripción',
            'valor_total': 'Valor total',
            'estado': 'Estado',
        }
        widgets = {
            'numero_pedido': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'numero_pedido': {'unique': 'Ya existe un pedido con ese número.'},
        }

    def clean_numero_pedido(self):
        numero = self.cleaned_data['numero_pedido'].strip()
        if not numero:
            raise forms.ValidationError('El número de pedido es obligatorio.')
        return numero

    def clean_cliente(self):
        cliente = self.cleaned_data['cliente'].strip()
        if not cliente:
            raise forms.ValidationError('El nombre del cliente es obligatorio.')
        return cliente

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion'].strip()
        if not descripcion:
            raise forms.ValidationError('La descripción del pedido es obligatoria.')
        return descripcion

    def clean_valor_total(self):
        valor = self.cleaned_data['valor_total']
        if valor <= 0:
            raise forms.ValidationError('El valor total debe ser mayor que cero.')
        return valor