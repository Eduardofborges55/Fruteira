from datetime import timedelta

from django.db import models
from django.utils import timezone

class Fruta(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    validade = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["validade", "nome"]
        verbose_name = "Fruta"
        verbose_name_plural = "Frutas"

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"

    @property
    def status_validade(self):
        hoje = timezone.localdate()
        if self.validade < hoje:
            return "vencida"
        if self.validade == hoje:
            return "vence_hoje"
        if self.validade <= hoje + timedelta(days=7):
            return "proxima"
        return "ok"
