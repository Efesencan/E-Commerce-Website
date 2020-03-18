from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = ['isActive', 'quantity','price','cost','name','modelNo', \
     'description','warrantyStatus','disturbuterInfo','categoryName','listedDate']
    
class BasketAdmin(admin.ModelAdmin):
    fields = ['cId', 'pId','quantity','totalPrice','purchasedDate','isPurchased']

class DeliveryAdmin(admin.ModelAdmin):
    fields = ['address', 'IsDelivered']

class ClientAdmin(admin.ModelAdmin):
    fields = ['name', 'email','address','taxNumber','fId']

class InvoiceAdmin(admin.ModelAdmin):
    fields = ['cId','bId', 'dId']

class FavouriteAdmin(admin.ModelAdmin):
    fields = ['cId','pId']

admin.site.register(Product,  ProductAdmin)
admin.site.register(Basket,    BasketAdmin)
admin.site.register(Delivery,  DeliveryAdmin)
admin.site.register(Client,    ClientAdmin)
admin.site.register(Invoice,   InvoiceAdmin)
admin.site.register(Favourite, FavouriteAdmin)