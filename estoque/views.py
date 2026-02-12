from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FrutaForm
from .models import Fruta


def lista_frutas(request):
    frutas = Fruta.objects.all()
    hoje = timezone.localdate()

    context = {
        "frutas": frutas,
        "total_itens": frutas.count(),
        "total_quantidade": sum(fruta.quantidade for fruta in frutas),
        "vencidas": sum(1 for fruta in frutas if fruta.validade < hoje),
        "vencem_hoje": sum(1 for fruta in frutas if fruta.validade == hoje),
        "proximas_sete": sum(
            1 for fruta in frutas if hoje < fruta.validade <= hoje + timedelta(days=7)
        ),
    }
    return render(request, "estoque/lista_frutas.html", context)


def criar_fruta(request):
    if request.method == "POST":
        form = FrutaForm(request.POST)
        if form.is_valid():
            form.save()
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
            form.save()
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
