from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from app import constants as const
from app.models import *
from django.db.models import Q
from django import forms
import json


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
                return signin(request)
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

def add_product_image(request):
    product_image = request.FILES.get('product-image')
    if product_image:
        binary_image = product_image.read()
        print(binary_image)
        return JsonResponse({'status_code': 200, 'message': 'Image converted to binary successfully'})
    else:
        return JsonResponse({'status_code': 400, 'message': 'No image file provided'})

def signout(request):
    if request.user.is_authenticated: logout(request)
    return redirect('signin')

def delete_account(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        signout(request)
        User.objects.filter(id=user_id).delete()
        messages.debug(request, 'Account has been deleted Successfully!')
    return redirect('signin')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

# add products
def products(request):
    fields = list(Field.objects.all().values())
    for field in fields:
        field_properties = FieldProperty.objects.filter(field_id=field.get('id'))
        properties = list()
        for field_property in field_properties:
            property = Property.objects.filter(id=field_property.property_id).values()
            properties.append(property[0])
        field['properties'] = properties
    print(fields)
    return render(request, 'components-products.html', {'fields': fields})

def add_product(request):
    return JsonResponse({'status_code': 200})

def manage(request):
    fields = Field.objects.all()
    field_types = FieldType.objects.all()
    properties = Property.objects.all()
    return render(request, 'components-manage.html', {'fields': fields, 'field_types': field_types, 'properties': properties})

# Fields
def add_field(request):
    data = json.loads(request.POST.get('data', '{}'))
    fields = dict()
    for field in data.get('field'):
        for key, value in field.items():
            fields[key] = value
    
    for label in data.get('label'):
        for key, value in label.items():
            fields[key] = value
    
    field = Field.objects.create(
        name=fields.get('field-name'),
        placeholder=fields.get('field-placeholder'),
        type=FieldType.objects.get(id=fields.get('field-type')),
        value=fields.get('field-value'),
        input_id=fields.get('field-id'),
        input_class=fields.get('field-class')
    )
    
    for property in data.get('property'):
        for key, value in property.items():
            field_property = Property.objects.filter(id=key).get()
            FieldProperty.objects.create(
                field=field,
                property=field_property
            )
    
    return JsonResponse({'status_code': 200, 'message': 'Field created successfully'})

def get_fields(request):
    try:
        fields = list(Field.objects.all().values())
        for field in fields:
            field_properties = FieldProperty.objects.filter(field_id=field.get('id'))
            properties = list()
            for field_property in field_properties:
                property = Property.objects.filter(id=field_property.property_id).values()
                properties.append(property[0])
            field['properties'] = properties
            field['type'] = FieldType.objects.filter(id=field.get('type_id')).values()[0]
        return JsonResponse({'status_code': 200, 'fields': fields})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': 'Failed to get fields'})

def delete_field(request):
    try:
        field_id = request.POST.get('field-id')
        field = Field.objects.get(id=field_id)
        field.delete()
        messages.success(request, 'Field deleted successfully')
        return redirect('/manage')
    except Exception as e:
        messages.error(request, f'Failed to delete Field! Error: {e}')
        return redirect('/manage')

# Property
def add_property(request):
    try:
        data = json.loads(request.POST.get('data', '{}'))
        property_name = str(data.get('property-name')).strip()
        property_tag = str(data.get('property-tag')).strip()
        property_value = str(data.get('property-value')).strip()
        property_type = str(data.get('property-type')).strip()
        property_description = str(data.get('property-description')).strip()
        Property.objects.create(
            name=property_name,
            tag = property_tag,
            value=property_value,
            type=property_type,
            description=property_description
        )
        return JsonResponse({'status_code': 200, 'message': 'Property created successfully'})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': f'Failed to Create Property! Error: {e}'})

def delete_property(request):
    try:
        property_id = request.POST.get('property-id')
        # field_property = FieldProperty.objects.get(id=property_id)
        # field_property.delete()
        messages.success(request, 'Property deleted successfully')
        return redirect('/manage')
    except Exception as e:
        messages.error(request, f'Failed to delete Property! Error: {e}')
        return redirect('/manage')

def add_input_type(request):
    try:
        data = json.loads(request.POST.get('data', '{}'))
        name = str(data.get('input-type-name')).strip()
        input_type = str(data.get('input-type-value')).strip()
        print(name, input_type)
        FieldType.objects.create(name=name, field_type=input_type)
        return JsonResponse({'status_code': 200, 'message': 'Input Type created successfully'})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': f'Failed to create Input Type! Error: {e}'})

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
