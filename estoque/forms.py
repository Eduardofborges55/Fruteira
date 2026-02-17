from django import forms

from .models import Fruta


class FrutaForm(forms.ModelForm):
    class Meta:
        model = Fruta
        fields = [
            "nome",
            "quantidade",
            "data_chegada",
            "preco_normal",
            "preco_promocional",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Banana prata"}),
            "quantidade": forms.NumberInput(attrs={"min": "0"}),
            "data_chegada": forms.DateInput(attrs={"type": "date"}),
            "preco_normal": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "preco_promocional": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }
