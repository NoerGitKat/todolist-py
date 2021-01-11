from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

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
    return render(request, 'currenttodos.html')
