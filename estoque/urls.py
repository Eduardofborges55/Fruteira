from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_frutas, name="lista_frutas"),
    path("frutas/nova/", views.criar_fruta, name="criar_fruta"),
    path("frutas/<int:fruta_id>/editar/", views.editar_fruta, name="editar_fruta"),
    path("frutas/<int:fruta_id>/excluir/", views.excluir_fruta, name="excluir_fruta"),
]
