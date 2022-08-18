from ast import Delete
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from Mensajes.models import Mensajes




def home(request):  #comentariosForms
    articulos = Entrada.objects.all().order_by('-id')[:3]
    nuevos = Mensajes.objects.filter(leido=False, nombre=request.user).count()
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            comentario = form.cleaned_data['comentario']
            obj = Comentario(nombre=nombre, comentario=comentario)
            obj.save()
            #Configurar Correo
            #asunto = form.cleaned_data['nombre']
            #mensaje = form.cleaned_data['comentario']
            #direccion = "entregafinal2022@yahoo.com"
            #destinatario = ["pameyari2529@gmail.com"]

            #send_mail(asunto,mensaje,direccion,destinatario)

            form = ComentarioForm()
            mensaje = "Gracias por tu comentario"
            return render(request,"bienvenida.html", {"articulos":articulos, "nuevos": nuevos, "mensaje":mensaje,"form":form})
    form = ComentarioForm()
    return render(request, "bienvenida.html", {"articulos":articulos, "nuevos":nuevos, "form":form})

@login_required
def entrada(request):
    if request.method == "POST":

        form = EntradaForm(request.POST, request.FILES)
        if form.is_valid():
            
            info= form.cleaned_data
            titulo = info["titulo"]
            subtitulo = info["subtitulo"]
            contenido = info["contenido"]
            imagen= info["imagen"]
            entrada = Entrada(titulo=titulo, subtitulo=subtitulo, contenido=contenido, autor=request.user, imagen=imagen)
            entrada.save()
            articulos = Entrada.objects.all().order_by('-id')[:3]
            #last_ten_in_ascending_order = reversed(last_ten)()
            return render(request, "bienvenida.html", {"articulos": articulos})
    else:
        form = EntradaForm()

    return render(request, "entradaForm.html", {"form":form})


def login_request(request):
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu = request.POST['username']
            clave = request.POST['password']
            usuario = authenticate(username = usu, password = clave)
            if usuario is not None:
                login(request, usuario)
                articulos = Entrada.objects.all().order_by('-id')[:3]
                nuevos = Mensajes.objects.filter(leido=False, nombre=request.user).count()
                return render(request, 'bienvenida.html', {'articulos':articulos, 'nuevos': nuevos, 'mensaje':f"Bienvenido {usuario}"})
            else:
                return render(request, 'loginForm.html', {'form':form, 'mensaje': 'Usuario o clave incorrecta'})
        else:
            return render(request, 'loginForm.html', {'form':form, 'mensaje':f"FORMULARIO INVALIDO"})
    else:
        form = AuthenticationForm()
    return render(request, 'loginForm.html', {'form':form})

def registrate(request):
    if request.method == "POST":

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]  # es igual a form.cleaned_data.get('username')
            form.save()
            # u = User.objects.get(username=username)
            # permission = Permission.objects.get(codename='view_personal')
            # u.user_permissions.add(permission)
            return render(request, "registro.html", {"mensaje":f"Usuario creado: { username }"})
    else:
        form = UserRegisterForm()

    return render(request, "registroForm.html", {"form":form})


@login_required
def agregarAvatar(request):
    if request.method == 'POST':
        formulario=AvatarForm(request.POST, request.FILES)
        if formulario.is_valid():
            try:
                avatarViejo=Avatar.objects.get(user=request.user)
                if(avatarViejo.imagen):
                    avatarViejo.delete()
            except:
                pass
            avatar=Avatar(user=request.user, imagen=formulario.cleaned_data['imagen'])
            avatar.save()
            return render(request, 'bienvenida.html', {'usuario':request.user, 'mensaje':'AVATAR AGREGADO EXITOSAMENTE'})
    else:
        formulario=AvatarForm()
    return render(request, 'agregarAvatar.html', {'formulario':formulario, 'usuario':request.user})


@login_required
def editarPerfil(request):
    usuario=request.user

    if request.method == 'POST':
        formulario=UserEditForm(request.POST, instance=usuario)
        if formulario.is_valid():
            informacion=formulario.cleaned_data
            usuario.email=informacion['email']
            usuario.password1=informacion['password1']
            usuario.password2=informacion['password2']
            usuario.save()

            return render(request, "bienvenida.html", {'usuario':usuario, 'mensaje':'PERFIL EDITADO EXITOSAMENTE'})
    else:
        formulario=UserEditForm(instance=usuario)
    return render(request, 'editarPerfil.html', {'formulario':formulario, 'usuario':usuario.username})


def Articulos(request):
    comentar=Comentarios.objects.all()
    return render(request,"entradas.html",{"comentar":comentar})

    
def inicio(request):
    return render(request,"bienvenida.html")


def detalleEntrada(request, id_entrada):
    try:
        entrada = Entrada.objects.get(id=id_entrada)
        comentarios = Comentarios.objects.filter(entrada_id=id_entrada)
    except:
        return render(request,"detalleEntrada.html",{"mensaje":'La entrada no existe'})
    return render(request,"detalleEntrada.html",{"entrada":entrada, "comentarios": comentarios})

def entradas(request):
    articulos = Entrada.objects.all().order_by('-fecha_ingreso')
    return render(request, "entradas.html", {"entradas":articulos})

@login_required
def editarEntrada(request, id_entrada):
    try:
        entrada = Entrada.objects.get(id=id_entrada)
    except:
        return render(request, "bienvenida.html", {'mensaje':'El articulo no existe'})
    if entrada.autor != request.user:
        return render(request, "bienvenida.html", {'mensaje':'Uds no es el autor del articulo'})

    if request.method == "POST":
        form = EntradaForm(request.POST, request.FILES)
        if form.is_valid():
            info = form.cleaned_data
            entrada.titulo = info["titulo"]
            entrada.subtitulo = info["subtitulo"]
            entrada.contenido = info["contenido"]
            entrada.autor=request.user
            if info["imagen"] != None:
                entrada.imagen = info["imagen"]
            entrada.save()
            return redirect('inicio')
    else:
        form = EntradaForm(initial={"titulo":entrada.titulo, "subtitulo":entrada.subtitulo,
                                    "contenido":entrada.contenido, "autor":request.user, "imagen":entrada.imagen})

    return render(request, "editarEntrada.html", {"form":form, "id_entrada":entrada.id})

def Nosotros(request):
    return render(request,"nosotros.html")


@login_required
def borrarEntrada(request, id_entrada):
    try:
        entrada = Entrada.objects.get(id=id_entrada)
    except:
        return render(request,"bienvenida.html",{"mensaje":'La entrada no existe'})

    entrada.delete()
    return redirect('inicio')
    

def comentarEntrada(request, id_entrada):
    
    if request.method == "POST":
        form = ComEntradaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            comentario = form.cleaned_data['comentario']
            obj = Comentarios(entrada_id = id_entrada, nombre=nombre, comentario=comentario)
            obj.save()
            entrada = Entrada.objects.get(id=id_entrada)
            comentarios = Comentarios.objects.filter(entrada_id=id_entrada)
            return render(request,"detalleEntrada.html", {"entrada": entrada, "comentarios": comentarios})
    form = ComEntradaForm()
    return render(request, "comEntrada.html", { "id_entrada": id_entrada, "form":form})
