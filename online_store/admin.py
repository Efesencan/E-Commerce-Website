from django.contrib import admin
from .models import Account
from .models import *
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    fields = ['isActive', 'quantity','price','cost','name','modelNo', \
     'description','warrantyStatus','disturbuterInfo','categoryName','listedDate']
    
class BasketAdmin(admin.ModelAdmin):
    fields = ['cId', 'pId','quantity','totalPrice','purchasedDate','isPurchased']

class DeliveryAdmin(admin.ModelAdmin):
    fields = ['address', 'IsDelivered']

class CustomerAdmin(admin.ModelAdmin):
    fields = ['name', 'email','address','taxNumber']

class InvoiceAdmin(admin.ModelAdmin):
    fields = ['cId','bId', 'dId']

class FavouriteAdmin(admin.ModelAdmin):
    fields = ['cId','pId']


class AccountAdmin(admin.ModelAdmin):
    model = Account

class CategoryAdmin(admin.ModelAdmin):
     fields = ['categoryName']

#This one is for authentication
admin.site.register(Account, AccountAdmin)

#rest is for models
admin.site.register(Product,  ProductAdmin)
admin.site.register(Basket,    BasketAdmin)
admin.site.register(Delivery,  DeliveryAdmin)
admin.site.register(Customer,    CustomerAdmin)
admin.site.register(Invoice,   InvoiceAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Category,  CategoryAdmin)