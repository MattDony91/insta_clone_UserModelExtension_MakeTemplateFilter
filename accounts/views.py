from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        if request.user.is_anonymous:
            form = CustomUserCreationForm()
        else:
            return render(request, 'error.html')
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        if request.user.is_anonymous:
            form = AuthenticationForm()
        else:
            return render(request, 'error.html')
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def user_page(request, id):
    user_info = get_object_or_404(User, id=id)
    context = {
        'user_info': user_info,
    }
    return render(request, 'accounts/user_page.html', context)


def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user
    if you != me:
        if me.followings.filter(id=id):
            me.followings.remove(you)
        else:
            me.followings.add(you)
    return redirect('accounts:user_page', id)


@require_POST
def delete(request, id):
    user_info = get_object_or_404(User, id=id)
    user = request.user
    if user == user_info:
        user.delete()
    return redirect('posts:index')


def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            # auth_login(request, request.user)f
            return redirect('posts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


def profile(request):
    return redirect('accounts:user_page', request.user.id)