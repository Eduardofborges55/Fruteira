from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from estoque.models import Fruta, StatusCiclo
from estoque.services import atualizar_ciclo_queryset


class Command(BaseCommand):
    help = "Atualiza status de ciclo das frutas (promocao, apodrecimento e descarte)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data",
            type=str,
            help="Data de referencia no formato YYYY-MM-DD (opcional).",
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
        atualizadas, descartadas = atualizar_ciclo_queryset(frutas, data_hoje)

        self.stdout.write(
            self.style.SUCCESS(
                f"Ciclo atualizado com sucesso em {data_hoje}: "
                f"{atualizadas} frutas processadas, {descartadas} descartadas."
            )
        )
