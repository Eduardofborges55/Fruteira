from django import forms

from .models import Fruta


class FrutaForm(forms.ModelForm):
    class Meta:
        model = Fruta
        fields = ["nome", "quantidade", "validade"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Banana prata"}),
            "quantidade": forms.NumberInput(attrs={"min": "0"}),
            "validade": forms.DateInput(attrs={"type": "date"}),
        }
