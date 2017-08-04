# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from doodoll_kit.decorators import jsonify
from doodoll_kit.utils.forms import errors_to_json
from .forms import ChangepwdForm, LoginForm, FindPwdForm, ResetPwdForm


@jsonify
def auth_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('member_index')
        # return dict(state=False, error=errors_to_json(form.errors))
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
    })


@jsonify
@login_required
def auth_reset_password(request):
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = form.cleaned_data.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return redirect('member_index')
        return dict(state=False, error=errors_to_json(form.errors))
    else:
        form=ChangepwdForm()
    return render(request, 'reset_password.html', {
        'form': form,
    })


@jsonify
def auth_find_password(request):
    return render(request, 'find_password.html', {})


def auth_logout(request):
    logout(request)
    return redirect('auth_login')