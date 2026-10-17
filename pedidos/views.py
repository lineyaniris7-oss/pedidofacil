from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PedidoForm
from .models import Pedido


@login_required
def listado_pedidos(request):
    q = request.GET.get("q", "").strip()
    pedidos = Pedido.objects.select_related("usuario")
    if q:
        pedidos = pedidos.filter(cliente__icontains=q)
    return render(request, "pedidos/listado.html", {"pedidos": pedidos, "q": q})


@login_required
def registrar_pedidos(request):
    form = PedidoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        pedido = form.save(commit=False)
        pedido.usuario = request.user
        pedido.save()
        messages.success(request, "Pedido registrado correctamente.")
        return redirect("pedidos:listado")
    return render(request, "pedidos/formulario.html", {"form": form, "titulo": "Nuevo pedido"})


@login_required
def detalle_pedidos(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    return render(request, "pedidos/detalle.html", {"pedido": pedido, "estados": Pedido.ESTADOS})


@login_required
def editar_pedidos(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    form = PedidoForm(request.POST or None, instance=pedido)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pedido actualizado correctamente.")
        return redirect("pedidos:detalle", id=pedido.id)
    return render(request, "pedidos/formulario.html", {"form": form, "titulo": "Editar pedido"})


@login_required
@require_POST
def eliminar_pedidos(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, "Pedido eliminado.")
    return redirect("pedidos:listado")


@login_required
@require_POST
def cambiar_estado(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    nuevo = request.POST.get("estado")
    if nuevo in dict(Pedido.ESTADOS):
        pedido.estado = nuevo
        pedido.save(update_fields=["estado"])
        messages.success(request, "Estado actualizado.")
    else:
        messages.error(request, "Estado no válido.")
    return redirect("pedidos:detalle", id=pedido.id)