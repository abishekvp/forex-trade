from django.contrib import admin
from client import models as client_models
# Register your models here.
admin.site.register(client_models.Cart)
admin.site.register(client_models.Wishlist)