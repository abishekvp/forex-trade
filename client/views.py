from django.shortcuts import render
from app import models as app_models
from client import models as client_models
from django.http import HttpResponse, JsonResponse
import base64

def index(request):
    products = app_models.Product.objects.all()
    for product in products:
        image = app_models.Image.objects.filter(product=product).first()
        if image:
            product.image = f"data:image/{image.extension};base64," + base64.b64encode(image.image).decode('utf-8')
        else:
            product.image = None
    return render(request, 'client/dashboard.html', {'products': products})

def category(request):
    products = app_models.Product.objects.all()
    for product in products:
        image = app_models.Image.objects.filter(product=product).first()
        if image:
            product.image = f"data:image/{image.extension};base64," + base64.b64encode(image.image).decode('utf-8')
        else:
            product.image = None
    return render(request, 'client/category.html', {'products': products})

def single_product(request, product_id=None):
    if not product_id:
        product = app_models.Product.objects.first()
    else:
        product = app_models.Product.objects.get(id=product_id)
    images = app_models.Image.objects.filter(product=product)
    for image in images:
        image.image = f"data:image/{image.extension};base64," + base64.b64encode(image.image).decode('utf-8')
    product.images = images
    return render(request, 'client/single-product.html', {'product': product})

def checkout(request):
    return render(request, 'client/checkout.html')

def add_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if client_models.Cart.objects.filter(user=request.user, product_id=product_id).exists():
            return JsonResponse({'status': 403, 'message': 'Product already in cart'})
        client_models.Cart.objects.create(
            user=request.user,
            product_id=product_id,
            quantity=1
        )   
        return JsonResponse({'status': 200, 'message': 'Product added to cart'})
    return JsonResponse({'status': 403, 'message': 'Invalid request'})

def cart(request):
    if request.user.is_authenticated:
        cart_items = client_models.Cart.objects.filter(user=request.user)
        for item in cart_items:
            product = app_models.Product.objects.get(id=item.product.id)
            image = app_models.Image.objects.filter(product=product).first()
            if image:
                item.product.image = f"data:image/{image.extension};base64," + base64.b64encode(image.image).decode('utf-8')
            else:
                item.product.image = None
        total = sum(int(item.product.price) for item in cart_items)
    else:
        cart_items = []
    return render(request, 'client/cart.html', {'cart_items': cart_items, 'total': total})

def confirmation(request):
    return render(request, 'client/confirmation.html')

def blog(request):
    return render(request, 'client/blog.html')

def single_blog(request):
    return render(request, 'client/single-blog.html')

def login(request):
    return render(request, 'client/login.html')

def tracking(request):
    return render(request, 'client/tracking.html')

def elements(request):
    return render(request, 'client/elements.html')

def contact(request):
    return render(request, 'client/contact.html')