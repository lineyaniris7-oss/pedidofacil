from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html, format_html_join


class RegistroForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

        self.fields["username"].help_text = ""

        reglas = password_validation.password_validators_help_texts()[1:]
        self.fields["password1"].help_text = format_html(
            "<ul>{}</ul>",
            format_html_join("", "<li>{}</li>", ((regla,) for regla in reglas)),
        )