from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.views.generic import ListView,TemplateView
from django.conf import settings
from rest_framework import viewsets, filters
from .serializers import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from rolepermissions.roles import assign_role
from rolepermissions.roles import remove_role
from rolepermissions.roles import get_user_roles
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.permissions import grant_permission
from rolepermissions.permissions import revoke_permission
from rolepermissions.permissions import available_perm_status
from rolepermissions.mixins import HasPermissionsMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#pagina de inicio
@login_required
# @has_permission_decorator('home')
def home(request):
    return render(request, 'home.html', {'title': 'Principal'})

# Login del usuario
def login_user(request):    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Esta cuenta ha sido desactivada')
                return redirect('login')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrecto')
            return redirect('login')
    return render(request, 'login.html', {'title': 'Login'})

# Logout del usuario
def logout_user(request):
    if request.GET:
        logout(request)
        return redirect('login')
        


class ListarUsuario(LoginRequiredMixin, HasPermissionsMixin, ListView):
    # required_permission = 'seguridad'
    model=Usuario
    context_object_name =  'usuarios'
    template_name="listaUsuario.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['privilegios'] = RolPermisoUsuario.objects.all()
    #     return context

@login_required
# @has_permission_decorator('seguridad')
def crearUsuario(request):
    context = {'title': 'Registrar Usuario'}
    if request.POST: 
        correo = request.POST['email']
        username = request.POST['username']
        password = Usuario.objects.make_random_password()
        print(password)
        user_form = UsuarioForm({
            'cedula': request.POST['cedula'],
            'nombre': request.POST['nombre'],
            'apellido': request.POST['apellido'],
            'username': username,
            'email': correo,
            'password1': password,
            'password2': password,
            'telefono': request.POST['telefono'],
            'estado': request.POST['estado'],
            'area': request.POST['area'],
            'cargo': request.POST['cargo'],
            'sexo': request.POST['sexo'],
            'observaciones': request.POST['observaciones']
        }, request.FILES)

        if user_form.is_valid():
            user_form.save()
            print("Usuario creado")
            lista = []
            lista.append(correo)
            desde = settings.EMAIL_HOST_USER
            asunto = "Bienvenido a Educacion Continua Fenix 4.0"
            link = 'http://127.0.0.1:8000/usuarios/%s/editarcontrasena/' % username
            # contenido = "<img src='https://i.ibb.co/wdDWrJJ/bienvenida.png' alt='bienvenida' height='400' width='400' border='0'>"+"<p>\nEstos son tus datos para login: \n</p><p>Usuario: %s \nContrasena: %s \n</p><p>En el sgte link puedes cambiar tu contraseña:</p><a href= %s >ailshdfsfecdsasdkdjfrnfrdhajwfessfakoqdnnndwdd</a>" % (username, password, link)
            contenido = "<p>\nEstos son tus datos para login: \n</p><p>Usuario: %s \nContrasena: %s \n</p><p>En el sgte <a href= %s >link</a> puedes cambiar tu contraseña.</p>" % (username, password, link)
            mail = EmailMessage(asunto, contenido, desde, lista)
            mail.content_subtype = "html"
            mail.send()

            usuario = Usuario.objects.order_by('-id')[0]
        
            roles = request.POST.getlist('rol')
            print(roles)
            modulos = request.POST.getlist('modulo')
            print(modulos)
            if len(roles) != len(modulos):
                flag_adm = False
                flag_doc = False
                for rol in roles:
                    if rol=='Administrador':
                        RolPermisoUsuario.objects.create(
                            usuario=usuario,
                            rol=rol
                        )
                        flag_adm=True
                        assign_role(usuario, 'administrador')
                        print("Se asigno rol Administrador")
                    elif rol=='Docente':
                        RolPermisoUsuario.objects.create(
                            usuario=usuario,
                            rol=rol
                        )
                        flag_doc=True
                        assign_role(usuario, 'docente')
                        print("Se asigno rol Docente")
                if flag_adm:
                    roles.pop(roles.index("Administrador"))
                if flag_doc:
                    roles.pop(roles.index("Docente"))
                print(len(roles)==len(modulos))
            
            for i in range(len(modulos)):
                RolPermisoUsuario.objects.create(
                    usuario=usuario,
                    rol=roles[i],
                    modulo=modulos[i]
                )
                if(modulos[i]=="Todos"):
                    if(roles[i]=="Observador"):
                        assign_role(usuario, 'observadorgeneral')
                    elif(roles[i]=="Analista"):
                        assign_role(usuario, 'analistageneral')
                    elif(roles[i]=="Coordinador"):
                        assign_role(usuario, 'coordinadorgeneral')
                elif(modulos[i]=="Academico"):
                    if(roles[i]=="Observador"):
                        assign_role(usuario, 'observadoracademico')
                    elif(roles[i]=="Analista"):
                        assign_role(usuario, 'analistaacademico')
                    elif(roles[i]=="Coordinador"):
                        assign_role(usuario, 'coordinadoracademico')
                elif(modulos[i]=="Administrativo"):
                    if(roles[i]=="Observador"):
                        assign_role(usuario, 'observadoradministrativo')
                    elif(roles[i]=="Analista"):
                        assign_role(usuario, 'analistaadministrativo')
                    elif(roles[i]=="Coordinador"):
                        assign_role(usuario, 'coordinadoradministrativo')
                elif(modulos[i]=="Financiero"):
                    if(roles[i]=="Observador"):
                        assign_role(usuario, 'observadorfinanciero')
                    elif(roles[i]=="Analista"):
                        assign_role(usuario, 'analistafinanciero')
                    elif(roles[i]=="Coordinador"):
                        assign_role(usuario, 'coordinadorfinanciero')
                elif(modulos[i]=="Comercial"):
                    if(roles[i]=="Observador"):
                        assign_role(usuario, 'observadorcomercial')
                    elif(roles[i]=="Analista"):
                        assign_role(usuario, 'analistacomercial')
                    elif(roles[i]=="Coordinador"):
                        assign_role(usuario, 'coordinadorcomercial')
                elif(modulos[i]=="Encuestas"):
                    if(roles[i]=="Observador"):
                        assign_role(usuario, 'observadorencuestas')
                    elif(roles[i]=="Analista"):
                        assign_role(usuario, 'analistaencuestas')
                    elif(roles[i]=="Coordinador"):
                        assign_role(usuario, 'coordinadorencuestas')

            context['id_usuario'] = usuario.id
        else:
            context['error'] = user_form.errors
            print(user_form.errors)

    return render(request, 'crearUsuario.html', context)

# @has_permission_decorator('edit_password')
def reestablecer_contrasena(request):
    context = {}
    if request.POST: 
        correo = request.POST['correo']
        username = Usuario.objects.filter(email=correo)
        if username:
            usuario = username[0].username
            lista = []
            lista.append(correo)
            desde = settings.EMAIL_HOST_USER
            asunto = "Reestablecimiento de contraseña"
            link = 'http://127.0.0.1:8000/usuarios/%s/editarcontrasena/' % usuario
            contenido = "<p>Hemos atendido tu petición para reestablecer la contraseña de tu usuario: %s.</p><p>En el sgte <a href= %s >link</a> puedes cambiar tu contraseña.</p>" % (usuario, link)
            mail = EmailMessage(asunto, contenido, desde, lista)
            mail.content_subtype = "html"  # Main content is now text/html
            mail.send()
            context['success'] = 'Se ha enviado un correo exitosamente a %s' % correo
            return render(request, 'reestablecerContrasena.html', context)
        else:
            context['error'] = 'ERROR: No se ha encontrado un usuario asociado a %s. Vuelve a intentar, recuerda ingresar el correo asociado a tu usuario' % correo
            return render(request, 'reestablecerContrasena.html', context)
    return render(request, 'reestablecerContrasena.html', context)

@login_required
# @has_permission_decorator('edit_password')
def modificar_contrasena(request, username):
    edit_contrasena = Usuario.objects.get(username=username)
    context = {
        'usuario': edit_contrasena
    }
    if request.POST:
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['username']
        email = edit_contrasena.email
        nombre = edit_contrasena.first_name
        apellido = edit_contrasena.last_name
        telefono = edit_contrasena.telefono
        estado = edit_contrasena.estado
        area = edit_contrasena.area
        cargo = edit_contrasena.cargo
        sexo = edit_contrasena.sexo
        cedula = edit_contrasena.cedula
        observaciones = edit_contrasena.observaciones

        user_form = UsuarioForm({
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'nombre': nombre,
            'telefono': telefono,
            'apellido': apellido,
            'estado': estado,
            'area': area,
            'cargo': cargo,
            'sexo': sexo,
            'cedula': cedula,
            'observaciones': observaciones
        }, request.FILES, instance=edit_contrasena)

        if user_form.is_valid():
            user_form.save()
            lista = []
            lista.append(email)
            desde = settings.EMAIL_HOST_USER
            asunto = "Cambio de contrasena exitoso"
            contenido = "<p>Hemos cambiado tu contraseña, estos son tus datos para login: \nUsuario: %s \nContrasena: %s</p>" % (username, password1)
            mail = EmailMessage(asunto, contenido, desde, lista)
            mail.content_subtype = "html"  # Main content is now text/html
            mail.send()
            context['success'] = '¡La contraseña ha sido modificada exitosamente! Hemos enviado un correo de confirmacion con tus nuevos datos'
        else:
            context['error'] = user_form.errors
            print(user_form.errors)
    return render(request, 'confirmarContrasena.html', context)

@login_required
# @has_permission_decorator('seguridad')
def viewUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    privilegios = RolPermisoUsuario.objects.filter(usuario=usuario.id)
    context = {
        'usuario': usuario,
        'privilegios': privilegios
    }
    return render(request, 'verUsuario.html', context)

#-------------------------API--------------------------------------------------------------
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
