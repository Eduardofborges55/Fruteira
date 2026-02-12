from django.contrib import admin
from .models import Fruta


@admin.register(Fruta)
class FrutaAdmin(admin.ModelAdmin):
    list_display = ("nome", "quantidade", "validade", "criado_em")
    search_fields = ("nome",)
    list_filter = ("validade",)
