from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TodoForm
from .models import Todo

# Create your views here.


def home(request):
    return render(request, 'index.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'pageTitle': 'Signup Page', 'form': UserCreationForm()})
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'signupuser.html', {'pageTitle': 'Signup Page', 'form': UserCreationForm(), 'error': 'That username has already been taken! Please choose a different one'})
        else:
            # Tell the user the passwords didn't match
            return render(request, 'signupuser.html', {'pageTitle': 'Signup Page', 'form': UserCreationForm(), 'error': 'Passwords do not match!'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'pageTitle': 'Login Page', 'form': AuthenticationForm()})
    if request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # Tell the user the passwords didn't match
            return render(request, 'loginuser.html', {'pageTitle': 'Login Page', 'form': AuthenticationForm(), 'error': 'Username or password incorrect.'})
        else:
            login(request, user)
            return redirect('currenttodos')


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completedAt__isnull=True)
    return render(request, 'currenttodos.html', {'currenttodos': todos})


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodo.html', {'form': TodoForm(), 'error': 'You just broke the form! Pass in normal data please.'})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, 'viewtodo.html', {'todo': todo, 'form': form})
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad information!'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.completedAt = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, completedAt__isnull=False)
    if request.method == 'GET':
        return render(request, 'completedtodos.html', {'todos': todos})
