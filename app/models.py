from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    image = models.TextField()

class Products(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()
    amount = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    rating = models.IntegerField()
    updated = models.DateField(auto_now_add=True)
    version = models.CharField(max_length=16)
    notes = models.TextField(max_length=128)
    image = models.TextField()

class Image(models.Model):
    image_binary = models.TextField()

class ImageMap(models.Model):
    class Meta:
        unique_together = ('product', 'image')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

