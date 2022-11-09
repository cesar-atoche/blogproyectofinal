from contextlib import ContextDecorator
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from blog.forms import articuloFormulario, categoriaFormulario, comentarioFormulario
from blog.models import Articulo, Categoria, Comentario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from blog.forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import User, AvatarFormulario
from blog.models import Avatar
from blog.forms import UserEditForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse

# inicio
def inicio(request):
    titulo = "Bienvenido"
    return render(request, "index.html", {"titulo": titulo})

@login_required
def iniciolo(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "indexlogueado.html", {"url":avatares[0].imagen.url})

def comentarios(request):
    titulo = "Comentarios"
    if request.method != "POST":
        formulario = comentarioFormulario()
    else:
        formulario = comentarioFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            articulo = Comentario(
                comentario=informacion["comentario"],
                nombre=informacion["nombre"],
                apellido=informacion["apellido"],
                email=informacion["email"],
                fecha=informacion["fecha"],
                estado=informacion["estado"],
            )
            articulo.save()
            return render(request, "respuesta.html", {"titulo": titulo})
    contenido = {"formulario": formulario, "titulo": titulo}
    return render(request, "comentarios.html", contenido)

class ComentarioList(ListView):
    model = Comentario
    template_name = "comentarios_list.html"


def listar_comentarios(request):
    todos_los_comentarios = Comentario.objects.all()
    contexto = {"comentarios_encontrados": todos_los_comentarios}
    return render(request, "comentarios_list.html", contexto)


class ComentarioDetalle(DetailView):
    model = Comentario
    template_name = "comentario_detalle.html"


class ClaseQueNecesitaLogin1(LoginRequiredMixin):
    class ComentarioCreacion(CreateView):
        model = Comentario
        fields = ["comentario", "nombre", "apellido", "email", "fecha"]

        def get_success_url(self):
            return reverse("ComentarioList")


class ClaseQueNecesitaLogin2(LoginRequiredMixin):
    class ComentarioUpdateView(UpdateView):
        model = Comentario
        success_url = "comentario/list"
        fields = ["comentario", "nombre", "apellido", "email", "fecha"]


class ClaseQueNecesitaLogin3(LoginRequiredMixin):
    class ComentarioDelete(DeleteView):

        model = Comentario
        success_url = "comentario/list"


def busqueda_de_comentario(request):
    return render(request, "buscar.html")


def buscar_comentario(request):
    if not request.GET["nombre"]:
        return HttpResponse("No enviaste datos")
    else:
        nombre_a_buscar = request.GET["nombre"]
        comentarios = Comentario.objects.filter(nombre=nombre_a_buscar)

        contexto = {"nombre": nombre_a_buscar, "comentarios_encontrados": comentarios}

        return render(request, "resultado_busqueda.html", contexto)


def login_request(request):
    titulo = "Login"

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)
                avatares = Avatar.objects.filter(user=request.user.id)
                return render(
                    request, "indexlogueado.html", {"mensaje": f"Bienvenido {usuario}","url":avatares[0].imagen.url}
                )
            else:

                return render(
                    request,
                    "index.html",
                    {"mensaje": "Error, datos incorrectos"},
                )

        else:

            return render(
                request, "index.html", {"mensaje": "Error, formulario erroneo"}
            )

    form = AuthenticationForm()

    return render(request, "login.html", {"form": form, "titulo": titulo})



def register(request):
    
    titulo = "Registro"
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username_capturado = form.cleaned_data["username"]
            contenido = {"mensaje": username_capturado, "titulo": titulo}
            form.save()

            return render(
                request, "respuesta.html", contenido
            )

    else:
        form = UserRegisterForm()

    return render(request, "registro.html", {"form": form, "titulo": titulo})



@login_required
def editarPerfil(request):
    titulo= "Edito"
    usuario = request.user
    contenido = {"titulo" : titulo , "mensaje" : usuario}

    if request.method == "POST":
        miFormulario = UserEditForm(request.POST)
        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion["email"]
            usuario.password1 = informacion["password1"]
            usuario.password2 = informacion["password2"]
            usuario.save()

            return render(request, "respuesta.html",contenido)

    else:
        
        miFormulario = UserEditForm(initial= {"email": usuario.email}
)

    return render(request, "editarPerfil.html", {"miFormulario": miFormulario, "usuario" : usuario})


@login_required
def agregarAvatar(request):
    if request.method == "POST":

        miFormulario = AvatarFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():

            u = User.objects.get(username=request.user)
            avatar = Avatar(user=u, imagen=miFormulario.cleaned_data["imagen"])
            avatar.save()
            return render(request, "index.html")

    else:

        miFormulario = AvatarFormulario()

    return render(request, "agregarAvatar.html", {"miFormulario": miFormulario})
