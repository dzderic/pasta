from django import forms
from django.contrib.auth.forms import AuthenticationForm
from bootstrap.forms import BootstrapModelForm, BootstrapMixin, Fieldset

from pasta_app.models import Repository

class BootstrapAuthForm(BootstrapMixin, AuthenticationForm):
    class Meta:
        layout = (
            Fieldset("Login", "username", "password"),
        )

class NewPastaForm(BootstrapModelForm):
    class Meta:
        model = Repository
        fields = ("name", )
