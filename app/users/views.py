from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm
from goods.models import Products


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()


    context = {
        'title': 'Авторизация',
        'form': form,
    }

    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }

    return render(request, 'users/registration.html', context)


def profile(request):
    context = {
        'title': 'Профиль'
    }

    return render(request, 'users/profile.html', context)

def cart(request):
    goods = Products.objects.order_by("?")

    goods = goods.filter(discount__gt=0)[:3]

    context = {
        'title': 'Корзина',
        'goods': goods,
    }

    return render(request, 'users/cart.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))
