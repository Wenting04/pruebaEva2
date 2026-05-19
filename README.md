# pruebaEva2 - Catálogo de películas

Este proyecto es una aplicación web dinámica en **Django** que funciona como un catálogo completo de películas en donde puede crear nuevos catálogos.

El proyecto se encuentra operativo en: [PythonAnywhere](https://wenting.pythonanywhere.com/)

---

## Características Principales

* ** Sistema de Autenticación y Roles:** Cuenta con tres niveles de acceso bien definidos (Superusuario/Administrador, Staff y Usuarios registrados) utilizando los mixins de seguridad de Django (`LoginRequiredMixin` y `UserPassesTestMixin`).
* ** Gestión de Contenido (CRUD Completo):** Los usuarios autorizados pueden **Crear, Leer, Actualizar y Borrar** (CRUD) posts de películas directamente desde la interfaz web.
* ** Seguridad en las Acciones:** Control a nivel de servidor; un usuario normal sólo puede modificar o eliminar las películas que él mismo ha publicado, mientras que el Staff/Admin tiene control total.
* ** Soporte Multimedia:** Permite la subida de imágenes de portada para cada película mediante el manejo de archivos `media`.

## Tecnologías Utilizadas

* **Backend:** Python 3.13 / Django 5.0.x
* **Base de Datos:** SQLite (Entorno de desarrollo y producción)
* **Despliegue / Hosting:** PythonAnywhere (WSGI)
* **Control de Versiones:** Git & GitHub

---
