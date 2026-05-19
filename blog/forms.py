# blog/forms.py
# Controla cómo se construye el formulario #

from django import forms
from django.forms import ModelForm

from .models import Post
from django.contrib.auth.models import User  # Para autores

class Dateinput(forms.DateInput):
    input_type = 'date'

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [ # Campos en formulario
            "autor", "titulo", "anno", "duracion", "pais", 
            "direccion", "guion", "reparto", "generos", "sinopsis", "imagen"
        ]
        widgets = { # Tipo de campo para rellenar
            # 'anno': Dateinput(), # El input que sea de fecha (DatePicker)
            'duracion': forms.NumberInput( # Sigue siendo num, pero podemos añadirle placeholder
                attrs={'placeholder': 'Duración en minutos', 'step': '1'}
            )
        }
        labels = { # Cambio de nombres ("apodos") # Sólo en la web, no en admin
            'titulo': 'Título',
            'anno': 'Año',
            'duracion': 'Duración',
            'pais': 'País',
            'direccion': 'Dirección',
            'guion': 'Guión',
            'generos': 'Géneros',
        }

    # Sólo staff o admin pueda editar autor de post al crear, si no, se oculta y se asigna autor al que está loggeado
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibimos el usuario de la vista

        super().__init__(*args, **kwargs)
        # Sacamos user
        # Lo guardamos
        # Pasamos el resto a super()

        if not (user.is_staff or user.is_superuser):
            # Si no es admin, ocultamos el campo autor
            self.fields.pop('autor')
        else:
            # Si es admin, que el campo autor sea un desplegable de todos los usuarios
            self.fields['autor'].queryset = User.objects.all()