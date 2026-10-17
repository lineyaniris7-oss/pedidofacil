from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RegistroForm


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("productos:listado")

    if request.method == "POST":
        usuario = authenticate(
            request,
            username=request.POST.get("username", ""),
            password=request.POST.get("password", ""),
        )
        next_url = request.POST.get("next", "")

        if usuario is not None:
            login(request, usuario)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("productos:listado")

        return render(
            request,
            "usuarios/login.html",
            {"error": "Usuario o contraseña incorrectos.", "next": next_url},
        )

    return render(request, "usuarios/login.html", {"next": request.GET.get("next", "")})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect("login")

def registro(request):
    if request.user.is_authenticated:
        return redirect("productos:listado")

    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, "Cuenta creada correctamente. ¡Bienvenido!")
        return redirect("productos:listado")

    return render(request, "usuarios/registro.html", {"form": form})