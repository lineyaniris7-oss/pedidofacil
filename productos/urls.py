from django.urls import path

from . import views

app_name = "productos"

urlpatterns = [
    path("", views.listado_productos, name="listado"),
    path("registrar/", views.registrar_productos, name="registrar"),
    path("detalle/<int:id>/", views.detalle_productos, name="detalle"),
    path("editar/<int:id>/", views.editar_productos, name="editar"),
    path("eliminar/<int:id>/", views.eliminar_productos, name="eliminar"),
]