from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('leer/', mensajes, name= 'mensajes'),
    path('formMensaje/<nombre>', formMensajes, name= 'formMensajes'),
    path('usuarios/', listaUsuarios, name= 'listaUsuarios'),
    path('mensaje/<msg_id>', mensaje, name='mensaje'),
    path('borrar/<msg_id>', borrar, name='borrar'),
]