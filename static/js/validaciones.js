// Validaciones del lado del cliente (JavaScript) para productos y pedidos.

const ESTADOS_PERMITIDOS = ["pendiente", "confirmado", "cancelado"];
const MAX_DESCRIPCION = 500;

// ---------- Mostrar y quitar errores ----------

function mostrarError(campo, mensaje) {
    limpiarError(campo);
    campo.classList.add("is-invalid");
    const aviso = document.createElement("div");
    aviso.className = "invalid-feedback error-js";
    aviso.textContent = mensaje;
    campo.insertAdjacentElement("afterend", aviso);
}

function limpiarError(campo) {
    campo.classList.remove("is-invalid");
    const siguiente = campo.nextElementSibling;
    if (siguiente && siguiente.classList.contains("error-js")) {
        siguiente.remove();
    }
}

// ---------- Reglas de productos ----------
// Cada regla recibe el valor del campo y devuelve el mensaje de error ("" si está bien).

const reglasProducto = {
    id_nombre: function (valor) {
        valor = valor.trim();
        if (valor === "") return "El nombre es obligatorio.";
        if (valor.length < 3) return "El nombre debe tener al menos 3 caracteres.";
        return "";
    },
    id_descripcion: function (valor) {
        if (valor.length > MAX_DESCRIPCION) {
            return "La descripción no puede superar los " + MAX_DESCRIPCION + " caracteres.";
        }
        return "";
    },
    id_precio: function (valor) {
        const numero = Number(valor);
        if (valor.trim() === "" || isNaN(numero) || numero <= 0) {
            return "El precio debe ser un número mayor que cero.";
        }
        return "";
    },
    id_cantidad_disponible: function (valor) {
        const numero = Number(valor);
        if (valor.trim() === "" || !Number.isInteger(numero) || numero < 0) {
            return "La cantidad debe ser un número entero igual o mayor que cero.";
        }
        return "";
    }
};

// ---------- Reglas de pedidos ----------

const reglasPedido = {
    id_numero_pedido: function (valor) {
        if (valor.trim() === "") return "El número del pedido es obligatorio.";
        return "";
    },
    id_cliente: function (valor) {
        if (valor.trim() === "") return "El nombre del cliente es obligatorio.";
        return "";
    },
    id_descripcion: function (valor) {
        if (valor.trim() === "") return "La descripción del pedido es obligatoria.";
        if (valor.length > MAX_DESCRIPCION) {
            return "La descripción no puede superar los " + MAX_DESCRIPCION + " caracteres.";
        }
        return "";
    },
    id_valor_total: function (valor) {
        const numero = Number(valor);
        if (valor.trim() === "" || isNaN(numero) || numero <= 0) {
            return "El valor total debe ser un número mayor que cero.";
        }
        return "";
    },
    id_estado: function (valor) {
        if (!ESTADOS_PERMITIDOS.includes(valor)) {
            return "Selecciona un estado válido: pendiente, confirmado o cancelado.";
        }
        return "";
    }
};

// ---------- Funciones que aplican las reglas ----------

function validarCampo(campo, regla) {
    const mensaje = regla(campo.value);
    if (mensaje) {
        mostrarError(campo, mensaje);
        return false;
    }
    limpiarError(campo);
    return true;
}

function activarValidacion(formulario, reglas) {
    // Al enviar: revisa todos los campos y, si hay errores, no deja enviar.
    formulario.addEventListener("submit", function (evento) {
        let primerError = null;
        for (const id in reglas) {
            const campo = formulario.querySelector("#" + id);
            if (campo && !validarCampo(campo, reglas[id]) && !primerError) {
                primerError = campo;
            }
        }
        if (primerError) {
            evento.preventDefault();
            primerError.focus();
        }
    });

    // Mientras el usuario corrige: vuelve a validar ese campo.
    for (const id in reglas) {
        const campo = formulario.querySelector("#" + id);
        if (!campo) continue;
        const tipoEvento = campo.tagName === "SELECT" ? "change" : "input";
        campo.addEventListener(tipoEvento, function () {
            validarCampo(campo, reglas[id]);
        });
    }
}

// ---------- Activar según el formulario que haya en la página ----------

document.addEventListener("DOMContentLoaded", function () {
    const formProducto = document.getElementById("formulario-producto");
    const formPedido = document.getElementById("formulario-pedido");

    if (formProducto) activarValidacion(formProducto, reglasProducto);
    if (formPedido) activarValidacion(formPedido, reglasPedido);
});