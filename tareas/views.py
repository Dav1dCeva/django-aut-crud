from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .formulario import formulario_tarea
from .models import Tareas
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html',)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario existente'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    tareas = Tareas.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tareas})

def task_incompleted(request):
    tasks = Tareas.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'completed': False})

def task_completed(request):
    tasks = Tareas.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html', {'tasks': tasks, 'completed': True})

@login_required
def task_detail(request,id):
    if request.method == 'GET':
        task= get_object_or_404(Tareas,pk=id,user=request.user)
        form=formulario_tarea(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form': form})
    else:
        try:
            task=get_object_or_404(Tareas, pk=id,user=request.user)
            form=formulario_tarea(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form': form, 'error':"Error al actualizar tarea"})

@login_required
def complete_task(request,id):
    task = get_object_or_404(Tareas,pk=id, user=request.user)
    if request.method =="POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required  
def tasks_completed(request):
     tareas = Tareas.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
     return render(request, 'tasks.html', {'tasks': tareas})

@login_required  
def delete_task(request,id):
    task = get_object_or_404(Tareas,pk=id, user=request.user)
    if request.method =="POST":
        task.delete()
        return redirect('tasks')

@login_required  
def crear_tarea(request):
    
    if request.method == 'GET':
        return render(request, 'crear_tasks.html',{
        'form': formulario_tarea
        })
    else:
        try:
            form=formulario_tarea(request.POST)
            nueva_tarea= form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'crear_tasks.html',{
        'form': formulario_tarea,
        'error': 'Porfavor escribe un dato valido'
            })

@login_required
def salir(request):
    logout(request)
    return redirect('home')


def regis_usuario(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user=authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña no validos'
        })
        else:
            login(request, user)
            return redirect('tasks')
