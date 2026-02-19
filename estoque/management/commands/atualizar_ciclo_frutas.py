from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from estoque.models import Fruta, RegraFruta, StatusCiclo


class Command(BaseCommand):
    help = "Atualiza status de ciclo das frutas (promocao, apodrecimento e descarte)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data",
            type=str,
            help="Data de referencia no formato YYYY-MM-DD (opcional).",
        )

    @staticmethod
    def _obter_regra(nome_fruta):
        regra = RegraFruta.objects.filter(nome_fruta__iexact=nome_fruta).first()
        if regra:
            return regra
        return RegraFruta(
            nome_fruta=nome_fruta,
            dias_para_promocao=4,
            dias_para_apodrecer=4,
            dias_ate_descarte_apos_apodrecer=3,
        )

    @staticmethod
    def _parse_data(valor):
        if not valor:
            return timezone.localdate()
        return datetime.strptime(valor, "%Y-%m-%d").date()

    @transaction.atomic
    def handle(self, *args, **options):
        data_hoje = self._parse_data(options.get("data"))
        frutas = Fruta.objects.exclude(status_ciclo=StatusCiclo.DESCARTADA)

        atualizadas = 0
        descartadas = 0

        for fruta in frutas:
            if not fruta.data_chegada:
                fruta.data_chegada = fruta.criado_em.date()

            regra = self._obter_regra(fruta.nome)

            fruta.data_promocao = fruta.data_chegada + timedelta(
                days=regra.dias_para_promocao
            )
            fruta.data_inicio_apodrecimento = fruta.data_chegada + timedelta(
                days=regra.dias_para_apodrecer
            )
            fruta.data_descarte = fruta.data_inicio_apodrecimento + timedelta(
                days=regra.dias_ate_descarte_apos_apodrecer
            )

            if fruta.preco_atual == 0:
                fruta.preco_atual = fruta.preco_normal

            if data_hoje >= fruta.data_descarte:
                fruta.status_ciclo = StatusCiclo.DESCARTADA
                fruta.quantidade = 0
                fruta.preco_atual = 0
                descartadas += 1
            elif data_hoje >= fruta.data_inicio_apodrecimento:
                fruta.status_ciclo = StatusCiclo.APODRECENDO
            elif data_hoje >= fruta.data_promocao:
                fruta.status_ciclo = StatusCiclo.PROMOCAO
                fruta.preco_atual = fruta.preco_promocional or fruta.preco_normal
            else:
                fruta.status_ciclo = StatusCiclo.DISPONIVEL
                fruta.preco_atual = fruta.preco_normal

            fruta.validade = fruta.data_descarte
            fruta.save()
            atualizadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Ciclo atualizado com sucesso em {data_hoje}: "
                f"{atualizadas} frutas processadas, {descartadas} descartadas."
            )
        )
