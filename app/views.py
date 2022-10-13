from re import X
from sqlite3 import Date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Med
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import date
from django.db.models import F

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                messages.info(request, "Sucessfully registered")
                return redirect("login")
        else:
            messages.info(request, "Password dosen't match")
            return redirect("register")

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('login')

    return render(request, 'login.html')


def update(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        expiry = request.POST['expiry']

        if Med.objects.filter(name=name).exists():
            med = Med.objects.get(name=name)
            x = med.quantity
            x = x + int(quantity)
            med.quantity = x
            med.save()

        else:
            med = Med(name=name, quantity=quantity, expiry=expiry)
            med.save()

    return render(request, 'update.html')


def dashboard(request):
    details = Med.objects.all().order_by('expiry').values()
    date = Date.today()

    x = 60
    for obj in Med.objects.all():
        d1 = obj.expiry
        d0 = date
        delta = d1-d0
        days = delta.days
        obj.time_left = days
        if days <= 0:
            obj.red = True
        elif days <= x:
            obj.yellow = True
        else:
            obj.green = True
        obj.save()

    # for i in range(1, num+1):
    #     mem = Med.objects.get(id=i)
    #     d1 = mem.expiry
    #     d0 = date
    #     delta = d1 - d0
    #     mem.time_left = delta.days
    #     mem.save()

    # Med.objects.update(time_left=F('expiry') - date)
    # Med.objects.update(time_left=F('time_left').days)
    # time_left = Med.objects.all().annotate(diff=F('expiry') - F('date'))
    return render(request, 'dashboard.html', {'details': details})
