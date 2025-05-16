from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    image = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512, null=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField(null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    price = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    rating = models.FloatField()
    updated = models.DateField(auto_now_add=True)
    version = models.CharField(max_length=16)
    notes = models.TextField(max_length=128, null=True, blank=True)
    created = models.DateField(auto_now=True)

class Image(models.Model):
    class Meta:
        unique_together = ('product', 'image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    name = models.CharField(max_length=64, null=True)
    image = models.BinaryField()
    extension = models.CharField(max_length=8, null=True)

class Form(models.Model):
    form_name = models.CharField(max_length=64, unique=True)
    form_value = models.CharField(max_length=64, unique=True)
    form_type = models.CharField(max_length=64)
    form_description = models.TextField(max_length=512)

class FieldType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    field_type = models.CharField(max_length=64, unique=True)

class Property(models.Model):
    name = models.CharField(max_length=64)
    tag = models.CharField(max_length=64)
    value = models.CharField(max_length=64, null=True)
    type = models.CharField(max_length=64, null=True)
    description = models.TextField(max_length=512, null=True)

class Field(models.Model):
    label = models.CharField(max_length=32, null=True)
    name = models.CharField(max_length=64, unique=True)
    placeholder = models.CharField(max_length=64)
    FIELD_TYPE_CHOICES = [
        ('text', 'text'),
        ('number', 'number'),
        ('date', 'date'),
        ('email', 'email'),
        ('phone', 'phone'),
    ]
    type = models.ForeignKey(FieldType, on_delete=models.CASCADE)
    value = models.CharField(max_length=64, blank=True)
    input_id = models.CharField(max_length=64)
    input_class = models.CharField(max_length=64)

class FieldProperty(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class FieldsValue(models.Model):
    class Meta:
        unique_together = ('field', 'product')
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.TextField()

class FormFieldMap(models.Model):
    class Meta:
        unique_together = ('form', 'field')
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

