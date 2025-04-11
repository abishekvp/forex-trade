
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

def index(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    return render(request, 'home.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('signin')

def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if username and email and password:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('signin')
            else:
                messages.error(request, 'Username or Email already exists')
                return redirect('signin')
        else:
            messages.error(request, 'Please fill all the fields to create an account')
    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            messages.error(request, 'Required username and password')
            return redirect('signin')
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials Please try again')
                return redirect('signin')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials Please try again')
    return render(request,'signin.html')

def signout(request):
    if request.user.is_authenticated: logout(request)
    return redirect('signin')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def handler400(request):
    return render(request, '400.html', status=400)
