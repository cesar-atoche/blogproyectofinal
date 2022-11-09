from django.urls import path
from blog.views import (
    inicio,
    listar_comentarios,
    ComentarioList,
    ClaseQueNecesitaLogin1,
    ClaseQueNecesitaLogin2,
    ClaseQueNecesitaLogin3,
    login_request,
    register,
    editarPerfil,
    agregarAvatar,
    iniciolo,
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", inicio, name="Inicio"),
    path("indexlo", iniciolo, name="IndexLo"),
    
    
    path("comentarios-lista/", listar_comentarios),
    path("comentario/list", ComentarioList.as_view(), name="ComentarioList"),
    # path("r'(?P<pk>\d+)^$'", ComentarioDetalle.as_view(), name="ComentarioDetail"),
    path(
        "comentario-nuevo/",
        ClaseQueNecesitaLogin1.ComentarioCreacion.as_view(),
        name="ComentarioNew",
    ),
    path(
        "editar/<pk>",
        ClaseQueNecesitaLogin2.ComentarioUpdateView.as_view(),
        name="ComentarioUpdate",
    ),
    path(
        "borrar/<pk>",
        ClaseQueNecesitaLogin3.ComentarioDelete.as_view(),
        name="ComentarioDelete",
    ),
    path("login/", login_request, name="Login"),
    path("register/", register, name="Register"),
    path("logout/", LogoutView.as_view(template_name="blog/logout.html"), name="Logout"),
    path("editarPerfil/", editarPerfil, name="EditarPerfil"),
    path("agregarAvatar/", agregarAvatar, name="AgregarAvatar"),
]
