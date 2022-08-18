from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from Mensajes.models import Mensajes
from Mensajes.forms import FormMensajes

# Create your views here.

nombre_temp =""

def mensajes(request):
    mensajes = Mensajes.objects.filter(nombre=request.user).order_by('-creado')
    return render(request, "Mensajes/mensajes.html", {'mensajes':mensajes})

def mensaje(request, msg_id):
    mensaje = Mensajes.objects.get(id=msg_id)
    mensaje.leido = True
    mensaje.save()
    return render(request, "Mensajes/mensaje.html", {'mensaje':mensaje})

# def enviar(request, nombre):
#     global nombre_temp
#     nombre_temp = nombre
#     form= FormMensajes(initial={"user":nombre, "autor":request.user})
#     return render(request, "Mensajes/formMensaje.html", {"formulario":form})

def formMensajes(request, nombre):
    if (request.method=="POST"):
        form= FormMensajes(request.POST)
        if form.is_valid():
            info= form.cleaned_data
            autor = request.user
            msj= info["mensaje"]
            mensaje = Mensajes(user=request.user, nombre=nombre, autor=autor, mensaje=msj)
            mensaje.save()
            return redirect('mensajes')
    else:
        form= FormMensajes(initial={"nombre":nombre, "autor":request.user})
    
    return render(request, "Mensajes/formMensaje.html", {"formulario":form, 'nombre':nombre})

def listaUsuarios(request):
    usuarios = User.objects.all().exclude(username=request.user)
    return render(request, "Mensajes/usuarios.html", {"usuarios":usuarios})


def borrar(request, msg_id):
    mensaje = Mensajes.objects.get(id=msg_id)
    mensaje.delete()
    return redirect('mensajes')