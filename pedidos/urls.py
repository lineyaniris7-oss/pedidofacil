from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.listado_pedidos, name="listado"),
    path("registrar/", views.registrar_pedidos, name="registrar"),
    path("detalle/<int:id>/", views.detalle_pedidos, name="detalle"),
    path("editar/<int:id>/", views.editar_pedidos, name="editar"),
    path("eliminar/<int:id>/", views.eliminar_pedidos, name="eliminar"),
    path("estado/<int:id>/", views.cambiar_estado, name="estado"),
]