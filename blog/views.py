# blog/views.py
# Controla la lógica de la request #

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# LoginRequiredMixin: Aunque hayamos hecho {% if user.is_authenticated %}, con LoginRequiredMixin, tratando de entrar por enlace, te redirige al Log In
    # Para usarlo, simplemente en class (aquí)
# UserPassesTestMixin: Para que sólo determinados usuarios puedan hacer dichas acciones
    # Para usarlo, crear función test_func

from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
# Q permite realizar consultas complejas usando operadores logicos como or, and
from .forms import PostForm


# = == CRUD == = #

# READ completo
class VistaListaPosts(ListView):
    model = Post
    template_name = "home.html"

    def get_queryset(self):

        # super().get_queryset() aplica después filtros personalizados
        queryset = super().get_queryset()

        # Capturar lo que el usuario escribe
        query = self.request.GET.get("q")
        
        # Q permite combinar condiciones usando operadores or. Filtra por titulo o sinopsis
        # icontains permite realizar búsquedas sin distinguir mayúsculas y minúsculas.
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(sinopsis__icontains=query)
            )

        return queryset

# READ uno
class VistaDetallePost(DetailView):
    model = Post
    template_name = "detalle_post.html"

# CREATE
class VistaCrearPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # Se asigna en forms.py
    template_name = "nuevo_post.html"

    # Explicación kwargs en forms.py
    # Obtener usuario
    def get_form_kwargs(self):
        """ Pasa el usuario actual al formulario para los campos dinamicos """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasamos el usuario al formulario
        return kwargs
    
    # Si admin, staff o usuario normal
    def form_valid(self, form):
        """ Se asigna automáticamente el autor si el usuario no es de Staff/Superuser """
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            # Si no es admin, el autor será el usuario logueado
            form.instance.autor = self.request.user
        return super().form_valid(form)

# UPDATE
class VistaActualizarPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm # Suponemos que el autor nunca cambia
    template_name = "actualizar_post.html"

    def get_success_url(self):
        """ Redirige al detalle_post después de actualizar correctamente """
        return reverse_lazy("detalle_post", kwargs={"pk": self.get_object().pk})

    # Incluso si no mostramos los usuarios, debemos de obtenerlo sí o sí por la función de form
    # Donde busca un usuario
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasamos el usuario al formulario
        return kwargs

    def test_func(self):
        """ Control de seguridad: debe ser propietario del post o Staff/Superuser """
        post = self.get_object()
        if (
            self.request.user == post.autor
            or self.request.user.is_staff
            or self.request.user.is_superuser
        ):
            return True
        else: 
            return False # 403 forbidden

    def handle_no_permission(self):
        """ Feedback con Django Messages si se intenta saltar la seguridad por vía URL """
        # Es decir, si intenta hacer /post/4/actualizar/ sin tener permisos, no te deja
        messages.error(self.request, "No tienes permiso para realizar esta acción")
        return redirect("detalle_post", pk=self.get_object().pk) # Recuerda los () después de .get_object
        # return redirect("home")

# DELETE
class VistaEliminarPost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "eliminar_post.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        """ Control de seguridad para el borrado """
        titulo = self.get_object()
        return(
            self.request.user == titulo.autor
            or self.request.user.is_staff
            or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para realizar esta acción")
        return redirect("home") # A casita