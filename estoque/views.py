from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FrutaForm
from .models import Fruta, StatusCiclo
from .services import atualizar_ciclo_fruta, atualizar_ciclo_queryset


def lista_frutas(request):
    hoje = timezone.localdate()
    atualizar_ciclo_queryset(Fruta.objects.exclude(status_ciclo=StatusCiclo.DESCARTADA), hoje)
    frutas = Fruta.objects.all()

    context = {
        "frutas": frutas,
        "total_itens": frutas.count(),
        "total_quantidade": sum(fruta.quantidade for fruta in frutas),
        "disponiveis": sum(
            1 for fruta in frutas if fruta.status_ciclo == StatusCiclo.DISPONIVEL
        ),
        "promocao": sum(
            1 for fruta in frutas if fruta.status_ciclo == StatusCiclo.PROMOCAO
        ),
        "apodrecendo": sum(
            1 for fruta in frutas if fruta.status_ciclo == StatusCiclo.APODRECENDO
        ),
        "descartadas": sum(
            1 for fruta in frutas if fruta.status_ciclo == StatusCiclo.DESCARTADA
        ),
        "vencidas": sum(
            1 for fruta in frutas if fruta.validade is not None and fruta.validade < hoje
        ),
        "vencem_hoje": sum(
            1
            for fruta in frutas
            if fruta.validade is not None and fruta.validade == hoje
        ),
        "proximas_sete": sum(
            1
            for fruta in frutas
            if fruta.validade is not None and hoje < fruta.validade <= hoje + timedelta(days=7)
        ),
    }
    return render(request, "estoque/lista_frutas.html", context)


def criar_fruta(request):
    if request.method == "POST":
        form = FrutaForm(request.POST)
        if form.is_valid():
            fruta = form.save()
            atualizar_ciclo_fruta(fruta, timezone.localdate())
            fruta.save()
            return redirect("lista_frutas")
    else:
        form = FrutaForm()

    return render(
        request,
        "estoque/form_fruta.html",
        {"form": form, "titulo": "Cadastrar Fruta", "botao": "Salvar fruta"},
    )


def editar_fruta(request, fruta_id):
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    if request.method == "POST":
        form = FrutaForm(request.POST, instance=fruta)
        if form.is_valid():
            fruta = form.save()
            atualizar_ciclo_fruta(fruta, timezone.localdate())
            fruta.save()
            return redirect("lista_frutas")
    else:
        form = FrutaForm(instance=fruta)

    return render(
        request,
        "estoque/form_fruta.html",
        {"form": form, "titulo": "Editar Fruta", "botao": "Atualizar fruta"},
    )


def excluir_fruta(request, fruta_id):
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    if request.method == "POST":
        fruta.delete()
        return redirect("lista_frutas")
    return render(request, "estoque/confirma_exclusao.html", {"fruta": fruta})
