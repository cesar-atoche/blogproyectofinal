from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class articuloFormulario(forms.Form):
    titulo = forms.CharField(max_length=200)
    texto = forms.CharField()
    fecha = forms.DateField()
    estado = forms.CharField(max_length=10)


class categoriaFormulario(forms.Form):
    nombre = forms.CharField(max_length=100)


class comentarioFormulario(forms.Form):
    comentario = forms.CharField()
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    email = forms.EmailField()
    fecha = forms.DateField()
    estado = forms.BooleanField()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repetir la contraseña", widget=forms.PasswordInput
    )

    class Meta:
        model= User
        # acá decia models = User pero me putea porque dice que User no esta definido. Donde deberia estar definido?
        fields = ["username", "email", "password1", "password2"]
        help_texts = {k: "" for k in fields}


class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Modificar E-mail")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repetir la contraseña", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
        help_texts = {k: "" for k in fields}

class AvatarFormulario():
   pass

class User():
   pass