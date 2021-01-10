from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.


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
            except IntegrityError:
                return render(request, 'signupuser.html', {'pageTitle': 'Signup Page', 'form': UserCreationForm(), 'error': 'That username has already been taken! Please choose a different one'})
        else:
            # Tell the user the passwords didn't match
            return render(request, 'signupuser.html', {'pageTitle': 'Signup Page', 'form': UserCreationForm(), 'error': 'Passwords do not match!'})
