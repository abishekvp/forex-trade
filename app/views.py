from typing import Optional, Dict, Any, List
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from app import constants as const
from app.models import Field, FieldProperty, Property, FieldType, Image, Product, Category
from django.db.models import Q
import json
import base64

def requires_group(group_name):
    """
    Decorator that checks if a user belongs to a specific group.
    Usage: @requires_group('admin')
    """
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            user_group = get_role(request.user)
            if not user_group or user_group != group_name.lower():
                messages.error(request, f'Access denied. {group_name} privileges required.')
                signout(request)
                return redirect('/signin')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



def get_role(user: User) -> Optional[str]:
    try:
        role = user.groups.first()
        return role.name.lower() if role else None
    except Exception as e:
        print(f"Error getting user role: {e}")
        return None

@login_required
@requires_group('admin')
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

@login_required
@requires_group('admin')
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not all([username, email, password]):
            messages.error(request, 'Please fill all the fields to create an account')
            return redirect('signup')
            
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, 'Username or Email already exists')
            return redirect('signup')
            
        try:
            user = User.objects.create_user(username, email, password)
            group = Group.objects.get_or_create(name='admin')[0]
            user.groups.add(group)
            authenticate(request, username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('signin')
        except Exception as e:
            messages.error(request, f'Error creating account: {e}')
            return redirect('signup')
            
    return render(request, 'signup.html')

@require_http_methods(["GET", "POST"])
def signin(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not all([username, password]):
            messages.error(request, 'Required username and password')
            return redirect('signin')
            
        try:
            if '@' in username:
                user = User.objects.get(email=username)
                username = user.username
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
            
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
            
        role = get_role(user)
        if not role:
            messages.error(request, 'User unable to signin')
            return redirect('signin')
            
        login(request, user)
        request.session['user_role'] = role
        return redirect(role)
        
    return render(request, 'signin.html')

def add_product_image(request):
    product_image = request.FILES.get('product-image')
    if product_image:
        binary_image = product_image.read()
        print(binary_image)
        return JsonResponse({'status_code': 200, 'message': 'Image converted to binary successfully'})
    else:
        return JsonResponse({'status_code': 400, 'message': 'No image file provided'})

@login_required
def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('signin')

@login_required
def delete_account(request: HttpRequest) -> HttpResponse:
    user_id = request.user.id
    logout(request)
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'Account has been deleted Successfully!')
    return redirect('signin')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

# add products
@login_required
@requires_group('admin')
def products(request: HttpRequest) -> HttpResponse:
    try:
        products = Product.objects.all()
        fields = Field.objects.all()
        for product in products:
            images = Image.objects.filter(product=product)
            product.images = list()
            for image in images:
                image_data = f"data:image/{image.extension};base64," + base64.b64encode(image.image).decode('utf-8')
                product.images.append({
                    'name': image.name,
                    'image': image_data
                })
        return render(request, 'components-products.html', {'products': products, 'fields': fields, 'categories': Category.objects.all()})
    except Exception as e:
        messages.error(request, f'Error loading products: {e}')
        return redirect('dashboard')

@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def add_product(request: HttpRequest) -> HttpResponse:
    try:
        product_image = request.FILES.get('product-image')
        rating = request.POST.get('product-rating')
        if rating:
            try:
                rating = float(rating)
                if rating < 0 or rating > 5:
                    messages.error(request, 'Rating must be between 0 and 5')
                    return redirect('products')
            except ValueError:
                messages.error(request, 'Invalid rating value')
                return redirect('products')
        product = Product.objects.create(
            name=request.POST.get('product-name'),
            description=request.POST.get('product-description'),
            category=Category.objects.get(id=request.POST.get('product-category')),
            value=request.POST.get('product-value'),
            price=request.POST.get('product-price'),
            rating=rating,
            version=request.POST.get('product-version'),
            notes=request.POST.get('product-notes') 
        )
        if product_image:
            Image.objects.create(
                product=product,
                name=product_image.name,
                image=product_image.read(),
                extension=product_image.name.split('.')[-1]
            )
        messages.success(request, 'Product created successfully')
    except Exception as e:
        messages.error(request, f'Failed to create product: {e}')
    url = request.POST.get('form-location-url')
    return redirect(url) if url else redirect('products')

@login_required
@requires_group('admin')
@require_http_methods(["GET", "POST"])
def product(request: HttpRequest, product_id: int) -> HttpResponse:
    try:
        product = Product.objects.get(id=product_id)
        image = Image.objects.filter(product=product).first()
        if image:
            image.image = f"data:image/{image.extension};base64," + base64.b64encode(image.image).decode('utf-8')
        else:
            image = None
        return render(request, 'components-product.html', {'product': product, 'image': image, 'categories': Category.objects.all()})
    except ObjectDoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('products')

@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def edit(request: HttpRequest, product_id: int) -> HttpResponse:
    try:
        product = Product.objects.get(id=product_id)
        product.name = request.POST.get('product-name')
        product.description = request.POST.get('product-description')
        if 'product-category' in request.POST:
            product.category = Category.objects.get(id=request.POST.get('product-category'))
        product.value = request.POST.get('product-value')
        product.price = request.POST.get('product-price')
        product.rating = request.POST.get('product-rating')
        product.version = request.POST.get('product-version')
        product.notes = request.POST.get('product-notes')
        product.save()
        
        if request.FILES.get('product-image'):
            image = Image.objects.filter(product=product).first()
            if image:
                image.image = request.FILES['product-image'].read()
                image.save()
            else:
                Image.objects.create(
                    product=product,
                    name=request.FILES['product-image'].name,
                    image=request.FILES['product-image'].read(),
                    extension=request.FILES['product-image'].name.split('.')[-1]
                )
                
        messages.success(request, 'Product updated successfully')
    except Exception as e:
        messages.error(request, f'Failed to update product: {e}')
    return redirect(f'/product/{product_id}')

@login_required
@requires_group('admin')
@require_http_methods(["GET"])
def delete(request: HttpRequest, product_id: int) -> HttpResponse:
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully')
    except ObjectDoesNotExist:
        messages.error(request, 'Product not found')
    return redirect('products')
    
@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def add_category(request: HttpRequest) -> HttpResponse:
    try:
        category = Category.objects.create(
            name=request.POST.get('category-name'),
            description=request.POST.get('category-description')
        )
        url = request.POST.get('form-location-url')
        messages.success(request, 'Category created successfully')
        if url:
            return redirect(url)
        return redirect('products')
    except Exception as e:
        messages.error(request, f'Failed to create category: {e}')
        return redirect('products')

@login_required
@requires_group('admin')
def manage(request: HttpRequest) -> HttpResponse:
    context = {
        'fields': Field.objects.all(),
        'field_types': FieldType.objects.all(),
        'properties': Property.objects.all()
    }
    return render(request, 'components-manage.html', context)

# Fields
@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def add_field(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.POST.get('data', '{}'))
        field_data = {}
        for field in data.get('field', []):
            field_data.update(field)
        for label in data.get('label', []):
            field_data.update(label)

        field = Field.objects.create(
            label=field_data.get('field-label'),
            name=field_data.get('field-name'),
            placeholder=field_data.get('field-placeholder'),
            type=FieldType.objects.get(id=field_data.get('field-type')),
            value=field_data.get('field-value'),
            input_id=field_data.get('field-id'),
            input_class=field_data.get('field-class')
        )

        for property_data in data.get('property', []):
            for property_id in property_data:
                FieldProperty.objects.create(
                    field=field,
                    property_id=property_id
                )

        return JsonResponse({'status_code': 200, 'message': 'Field created successfully'})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': f'Failed to create field: {e}'})

@login_required
@requires_group('admin')
def get_fields(request: HttpRequest) -> JsonResponse:
    try:
        fields = Field.objects.all().prefetch_related(
            'fieldproperty_set__property', 
            'type'
        ).values()
        
        for field in fields:
            field['properties'] = [
                prop.property for prop in field.fieldproperty_set.all()
            ]
            field['type'] = field.type
            
        return JsonResponse({'status_code': 200, 'fields': list(fields)})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': f'Failed to get fields: {e}'})

@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def delete_field(request: HttpRequest) -> HttpResponse:
    try:
        field_id = int(request.POST.get('field-id'))
        Field.objects.filter(id=field_id).delete()
        messages.success(request, 'Field deleted successfully')
    except Exception as e:
        messages.error(request, f'Failed to delete Field: {e}')
    return redirect('manage')

# Property
@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def add_property(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.POST.get('data', '{}'))
        Property.objects.create(
            name=str(data.get('property-name')).strip(),
            tag=str(data.get('property-tag')).strip(),
            value=str(data.get('property-value')).strip(),
            type=str(data.get('property-type')).strip(),
            description=str(data.get('property-description')).strip()
        )
        return JsonResponse({'status_code': 200, 'message': 'Property created successfully'})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': f'Failed to create Property: {e}'})

@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def delete_property(request: HttpRequest) -> HttpResponse:
    try:
        property_id = request.POST.get('property-id')
        Property.objects.filter(id=property_id).delete()
        messages.success(request, 'Property deleted successfully')
    except Exception as e:
        messages.error(request, f'Failed to delete Property: {e}')
    return redirect('manage')

@login_required
@requires_group('admin')
@require_http_methods(["POST"])
def add_input_type(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.POST.get('data', '{}'))
        FieldType.objects.create(
            name=str(data.get('input-type-name')).strip(),
            field_type=str(data.get('input-type-value')).strip()
        )
        return JsonResponse({'status_code': 200, 'message': 'Input Type created successfully'})
    except Exception as e:
        return JsonResponse({'status_code': 403, 'message': f'Failed to create Input Type: {e}'})

# Components

@login_required
@requires_group('admin')
def components(request: HttpRequest) -> HttpResponse:
    return render(request, 'components.html')

@login_required
@requires_group('admin')
def components_alerts(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-alerts.html')

@login_required
@requires_group('admin')
def components_accordion(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-accordion.html')

@login_required
@requires_group('admin')
def components_badges(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-badges.html')

@login_required
@requires_group('admin')
def components_breadcrumbs(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-breadcrumbs.html')

@login_required
@requires_group('admin')
def components_buttons(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-buttons.html')

@login_required
@requires_group('admin')
def components_cards(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-cards.html')

@login_required
@requires_group('admin')
def components_carousel(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-carousel.html')

@login_required
@requires_group('admin')
def components_list_group(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-list-group.html')

@login_required
@requires_group('admin')
def components_modal(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-modal.html')

@login_required
@requires_group('admin')
def components_tabs(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-tabs.html')

@login_required
@requires_group('admin')
def components_pagination(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-pagination.html')

@login_required
@requires_group('admin')
def components_progress(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-progress.html')

@login_required
@requires_group('admin')
def components_spinners(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-spinners.html')

@login_required
@requires_group('admin')
def components_tooltips(request: HttpRequest) -> HttpResponse:
    return render(request, 'components-tooltips.html')

@login_required
@requires_group('admin')
def forms_elements(request: HttpRequest) -> HttpResponse:
    return render(request, 'forms-elements.html')

@login_required
@requires_group('admin')
def forms_layouts(request: HttpRequest) -> HttpResponse:
    return render(request, 'forms-layouts.html')

@login_required
@requires_group('admin')
def forms_editors(request: HttpRequest) -> HttpResponse:
    return render(request, 'forms-editors.html')

@login_required
@requires_group('admin')
def forms_validation(request: HttpRequest) -> HttpResponse:
    return render(request, 'forms-validation.html')

@login_required
@requires_group('admin')
def tables_general(request: HttpRequest) -> HttpResponse:
    return render(request, 'tables-general.html')

@login_required
@requires_group('admin')
def tables_data(request: HttpRequest) -> HttpResponse:
    return render(request, 'tables-data.html')

@login_required
@requires_group('admin')
def charts_chartjs(request: HttpRequest) -> HttpResponse:
    return render(request, 'charts-chartjs.html')

@login_required
@requires_group('admin')
def charts_apexcharts(request: HttpRequest) -> HttpResponse:
    return render(request, 'charts-apexcharts.html')

@login_required
@requires_group('admin')
def charts_echarts(request: HttpRequest) -> HttpResponse:
    return render(request, 'charts-echarts.html')

@login_required
@requires_group('admin')
def icons_bootstrap(request: HttpRequest) -> HttpResponse:
    return render(request, 'icons-bootstrap.html')

@login_required
@requires_group('admin')
def icons_remix(request: HttpRequest) -> HttpResponse:
    return render(request, 'icons-remix.html')

@login_required
@requires_group('admin')
def icons_boxicons(request: HttpRequest) -> HttpResponse:
    return render(request, 'icons-boxicons.html')

@login_required
@requires_group('admin')
def users_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'users-profile.html')

@login_required
@requires_group('admin')
def pages_faq(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages-faq.html')

@login_required
@requires_group('admin')
def pages_contact(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages-contact.html')

def pages_error_404(request: HttpRequest) -> HttpResponse:
    return render(request, '404.html')

@login_required
@requires_group('admin')
def pages_blank(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages-blank.html')
