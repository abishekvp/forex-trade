from django.urls import path
from client import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='client')
]