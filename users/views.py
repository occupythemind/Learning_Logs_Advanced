from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.conf import settings
from django.contrib import messages
from functools import wraps

def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('learning_logs:home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@redirect_authenticated_user
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('learning_logs:home')
        else:
            messages.error(request, settings.INVALID_CRED)
    return render(request, 'users/login.html')

@redirect_authenticated_user
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            login(request, new_user)
            return redirect('learning_logs:home')
        else:
            print(form.errors)  # debug if needed
    return render(request, 'users/signup.html')

@login_required
def log_out(request):
    '''Just return the logout page'''
    return render(request, 'users/loggedout.html')