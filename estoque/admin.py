from django.contrib import admin
from .models import Fruta, RegraFruta


@admin.register(Fruta)
class FrutaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "quantidade",
        "status_ciclo",
        "data_chegada",
        "data_promocao",
        "data_descarte",
        "preco_atual",
    )
    search_fields = ("nome",)
    list_filter = ("status_ciclo", "data_chegada")


@admin.register(RegraFruta)
class RegraFrutaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_fruta",
        "dias_para_promocao",
        "dias_para_apodrecer",
        "dias_ate_descarte_apos_apodrecer",
    )
    search_fields = ("nome_fruta",)
