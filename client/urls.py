from django.urls import path
from client import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='client'),
    path('index', views.index),
    path('category', views.category, name='client-category'),
    path('single-product', views.single_product, name='client-single'),
    path('checkout', views.checkout, name='client-checkout'),
    path('cart', views.cart, name='client-cart'),
    path('add-cart', views.add_cart),
    path('confirmation', views.confirmation, name='client-confirmation'),
    path('blog', views.blog, name='client-blog'),
    path('single-blog', views.single_blog, name='client-single'),
    path('login', views.login, name='client-login'),
    path('tracking', views.tracking, name='client-tracking'),
    path('elements', views.elements, name='client-elements'),
    path('contact', views.contact, name='client-contact'),

]