from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProductoForm
from .models import Producto


@login_required
def listado_productos(request):
    q = request.GET.get("q", "").strip()
    productos = Producto.objects.all()
    if q:
        productos = productos.filter(nombre__icontains=q)
    return render(request, "productos/listado.html", {"productos": productos, "q": q})


@login_required
def registrar_productos(request):
    form = ProductoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Producto creado correctamente.")
        return redirect("productos:listado")
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Nuevo producto"})


@login_required
def detalle_productos(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "productos/detalle.html", {"producto": producto})


@login_required
def editar_productos(request, id):
    producto = get_object_or_404(Producto, id=id)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect("productos:detalle", id=producto.id)
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Editar producto"})


@login_required
@require_POST
def eliminar_productos(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado.")
    return redirect("productos:listado")