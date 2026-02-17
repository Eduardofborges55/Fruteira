from datetime import timedelta

from django.db import models
from django.utils import timezone


class StatusCiclo(models.TextChoices):
    DISPONIVEL = "disponivel", "Disponivel"
    PROMOCAO = "promocao", "Promocao"
    APODRECENDO = "apodrecendo", "Apodrecendo"
    DESCARTADA = "descartada", "Descartada"


class RegraFruta(models.Model):
    nome_fruta = models.CharField(max_length=100, unique=True)
    dias_para_promocao = models.PositiveSmallIntegerField(default=4)
    dias_para_apodrecer = models.PositiveSmallIntegerField(default=4)
    dias_ate_descarte_apos_apodrecer = models.PositiveSmallIntegerField(default=3)

    class Meta:
        ordering = ["nome_fruta"]
        verbose_name = "Regra de fruta"
        verbose_name_plural = "Regras de frutas"

    def __str__(self):
        return self.nome_fruta


class Fruta(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    validade = models.DateField(null=True, blank=True)
    data_chegada = models.DateField(null=True, blank=True)
    status_ciclo = models.CharField(
        max_length=20, choices=StatusCiclo.choices, default=StatusCiclo.DISPONIVEL
    )
    data_promocao = models.DateField(null=True, blank=True)
    data_inicio_apodrecimento = models.DateField(null=True, blank=True)
    data_descarte = models.DateField(null=True, blank=True)
    preco_normal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome", "data_chegada"]
        verbose_name = "Fruta"
        verbose_name_plural = "Frutas"

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"

    @property
    def status_validade(self):
        if not self.validade:
            return "ok"
        hoje = timezone.localdate()
        if self.validade < hoje:
            return "vencida"
        if self.validade == hoje:
            return "vence_hoje"
        if self.validade <= hoje + timedelta(days=7):
            return "proxima"
        return "ok"
