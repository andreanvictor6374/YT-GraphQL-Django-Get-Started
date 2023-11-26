from django.contrib import admin
from .models import Books, Customer, Order
# Register your models here.
admin.site.register(Books)
admin.site.register(Customer)
admin.site.register(Order)