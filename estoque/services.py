from datetime import timedelta

from .models import RegraFruta, StatusCiclo


def obter_regra(nome_fruta):
    regra = RegraFruta.objects.filter(nome_fruta__iexact=nome_fruta).first()
    if regra:
        return regra
    return RegraFruta(
        nome_fruta=nome_fruta,
        dias_para_promocao=4,
        dias_para_apodrecer=4,
        dias_ate_descarte_apos_apodrecer=3,
    )


def atualizar_ciclo_fruta(fruta, data_hoje):
    if not fruta.data_chegada:
        fruta.data_chegada = fruta.criado_em.date()

    regra = obter_regra(fruta.nome)

    fruta.data_promocao = fruta.data_chegada + timedelta(days=regra.dias_para_promocao)
    fruta.data_inicio_apodrecimento = fruta.data_chegada + timedelta(
        days=regra.dias_para_apodrecer
    )
    fruta.data_descarte = fruta.data_inicio_apodrecimento + timedelta(
        days=regra.dias_ate_descarte_apos_apodrecer
    )

    if data_hoje >= fruta.data_descarte:
        fruta.status_ciclo = StatusCiclo.DESCARTADA
        fruta.quantidade = 0
        fruta.preco_atual = 0
    elif data_hoje >= fruta.data_promocao:
        fruta.status_ciclo = StatusCiclo.PROMOCAO
        fruta.preco_atual = fruta.preco_promocional or fruta.preco_normal
    elif data_hoje >= fruta.data_inicio_apodrecimento:
        fruta.status_ciclo = StatusCiclo.APODRECENDO
        fruta.preco_atual = fruta.preco_promocional or fruta.preco_normal
    else:
        fruta.status_ciclo = StatusCiclo.DISPONIVEL
        fruta.preco_atual = fruta.preco_normal

    fruta.validade = fruta.data_descarte
    return fruta


def atualizar_ciclo_queryset(queryset, data_hoje):
    atualizadas = 0
    descartadas = 0

    for fruta in queryset:
        atualizar_ciclo_fruta(fruta, data_hoje)
        fruta.save()
        atualizadas += 1
        if fruta.status_ciclo == StatusCiclo.DESCARTADA:
            descartadas += 1

    return atualizadas, descartadas
