
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
        return render(request, 'home.html')
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

def products(request):
    return render(request, 'components-products.html')

# Components

def components(request):
    return render(request, 'components.html')

def components_alerts(request):
    return render(request, 'components-alerts.html')

def components_accordion(request):
    return render(request, 'components-accordion.html')

def components_badges(request):
    return render(request, 'components-badges.html')

def components_breadcrumbs(request):
    return render(request, 'components-breadcrumbs.html')

def components_buttons(request):
    return render(request, 'components-buttons.html')

def components_cards(request):
    return render(request, 'components-cards.html')

def components_carousel(request):
    return render(request, 'components-carousel.html')

def components_list_group(request):
    return render(request, 'components-list-group.html')

def components_modal(request):
    return render(request, 'components-modal.html')

def components_tabs(request):
    return render(request, 'components-tabs.html')

def components_pagination(request):
    return render(request, 'components-pagination.html')

def components_progress(request):
    return render(request, 'components-progress.html')

def components_spinners(request):
    return render(request, 'components-spinners.html')

def components_tooltips(request):
    return render(request, 'components-tooltips.html')

def forms_elements(request):
    return render(request, 'forms-elements.html')

def forms_layouts(request):
    return render(request, 'forms-layouts.html')

def forms_editors(request):
    return render(request, 'forms-editors.html')

def forms_validation(request):
    return render(request, 'forms-validation.html')

def tables_general(request):
    return render(request, 'tables-general.html')

def tables_data(request):
    return render(request, 'tables-data.html')

def charts_chartjs(request):
    return render(request, 'charts-chartjs.html')

def charts_apexcharts(request):
    return render(request, 'charts-apexcharts.html')

def charts_echarts(request):
    return render(request, 'charts-echarts.html')

def icons_bootstrap(request):
    return render(request, 'icons-bootstrap.html')

def icons_remix(request):
    return render(request, 'icons-remix.html')

def icons_boxicons(request):
    return render(request, 'icons-boxicons.html')

def users_profile(request):
    return render(request, 'users-profile.html')

def pages_faq(request):
    return render(request, 'pages-faq.html')

def pages_contact(request):
    return render(request, 'pages-contact.html')

def pages_error_404(request):
    return render(request, '404.html')

def pages_blank(request):
    return render(request, 'pages-blank.html')
