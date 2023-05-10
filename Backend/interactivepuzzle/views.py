from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created. You can log in now!')
            return redirect('index.html')

def login(request):
    return render(request,'login.html')


def index(request):
    return render(request, 'index.html')
