from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required  
def tasks(request):   #mostrar las tareas del usuario
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks' : tasks})

def delete_task(request, task_id):   #eliminar tarea
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def task_detail(request, task_id):   #vista de las tareas
    if request.method == 'GET':
            task = get_object_or_404(Task, pk=task_id)
            form = TaskForm(instance=task)
            return render(request, 'task_detail.html', {'task' : task, 'form' : form})
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')

def create_task(request):  #creacion de nuestra tarea
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form' : TaskForm
        })
    else: 
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False) 
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form' : TaskForm,
                'error' : 'Porfavor ingrese un dato valido'
            })

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user = Group.objects.get(name='user')
                user.groups.add(user)
                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    "error" : 'usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form' : UserCreationForm,
            "error" : 'contraseñas no coinciden'
        })
    
def signout(request):
    
    logout(request)
    return redirect('home')
                
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html',{
        'form' : AuthenticationForm
    })
        
    else:
        user = authenticate(request, username=request.POST ['username'], password=request.POST ['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form' : AuthenticationForm,
                'error' : 'Nombre o contraseña incorrectos'
            })
        
        else:
            login(request, user)
            return redirect('tasks')
        
@permission_required('auth.view_user', raise_exception=True)
def administrador(request):
    users = User.objects.all()
    return render(request, 'administrador.html', {'users': users})













    
