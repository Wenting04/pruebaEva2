from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    # Determina los campos que se va a mostrar en la lista de objetos
    list_display = (
        "autor", # Autor del post
        "titulo", "anno", "duracion", "pais", "direccion",
        "guion", "reparto", "generos",  "sinopsis", "imagen",
    )

admin.site.register(Post, PostAdmin)