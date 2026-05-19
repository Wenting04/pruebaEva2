# blog/urls.py
from django.urls import path
from .views import (
    VistaListaPosts, 
    VistaDetallePost, 
    VistaCrearPost,
    VistaActualizarPost,
    VistaEliminarPost
)

urlpatterns = [
    path("post/<int:pk>/eliminar/", VistaEliminarPost.as_view(), name="eliminar_post"),
    path("post/<int:pk>/actualizar/", VistaActualizarPost.as_view(), name="actualizar_post"),
    path("post/nuevo/", VistaCrearPost.as_view(), name="nuevo_post"),
    path("post/<int:pk>/", VistaDetallePost.as_view(), name="detalle_post"),
    path("", VistaListaPosts.as_view(), name="home"),
]