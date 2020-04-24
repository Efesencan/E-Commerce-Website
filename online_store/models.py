from django.db import models
from django.contrib.auth.models import AbstractUser
###On delete de oluyor bilmiyoruz!!!!!!!


class Account(AbstractUser):
    pass

# https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/models/


class Customer(models.Model):
    cId       = models.AutoField(primary_key=True)
    address   = models.CharField(max_length=500, null=True)
    taxNumber = models.IntegerField(null =True)  

    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )

class ProductManager(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
    )
class SalesManager(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
    )

# Create your models here.
class Product(models.Model):
    ### Primary Key
    pId = models.AutoField(primary_key=True) 
    
    ### Table Specific Fields
    isActive         = models.NullBooleanField()

    price            = models.FloatField()
    oldPrice         = models.FloatField()
    stock            = models.IntegerField()  
    imgSrc           = models.CharField(max_length=100)
    name             = models.CharField(max_length=50) # TEXT 
    
    cost             = models.FloatField()
    
    modelNo          = models.CharField(max_length=50) # TEXT ,BV200423 universal code
    description      = models.CharField(max_length=500) # TEXT
    warrantyStatus   = models.IntegerField()
    disturbuterInfo  = models.CharField(max_length=100) #TEXT
    categoryName     = models.ForeignKey('Category', null = True,on_delete = models.SET_NULL)
    listedDate       = models.DateField()

class Category(models.Model): # kategorinin son ürünü silindiğinde kategori de silinsin mi???
    categoryName = models.CharField(max_length=80, primary_key=True)
    categoryIconScr = models.CharField(max_length=80)

# bir müşterinin birden fazla ürün alması, sepetini görmesi,
# eski siparişlerini görüntülemesi özellikleri
# en son bu class invoice de kullanılacak ürün tarafı olacak, ie bi
# her transactionda Client ve pIdleri söyleyebilmeli
# örneğin gün1 x kişisi ürün 1 ve ürün 2 aldı. gün2 x kişisi bu sefere ürün3 ürün4 ü aldı
# bize gün1 de x kişisinin ürün1 ve ürün 2 aldığını söylebilmeli aynı şekilde ürün3 farklı 
# bir alışveriş olduğunu

class Basket(models.Model):
    bId            = models.AutoField(primary_key=True)
    cId            = models.ForeignKey('Customer', null = True,on_delete = models.SET_NULL)
    pId            = models.ForeignKey('Product', null = True,on_delete = models.SET_NULL) ##### değiştirsek 
    quantity       = models.IntegerField()
    totalPrice     = models.FloatField()
    purchasedDate  = models.DateField()
    isPurchased    = models.NullBooleanField()

    class Meta:
        unique_together = (('bId', 'cId'),)

 #   def Purchase():
  #      isPurchased =True
 #   def SeeMyBasket():
        # filter by isPurchased == False
 #   def SeeMyOldPurchases ():
        #filter by isPurchased == True
        #
        
#        Gok p1
#        Gok p2
#        gok p3
#        gok p4
        

class Delivery(models.Model):
    
    dId            = models.AutoField(primary_key=True)
    address        = models.CharField(max_length=500)
    IsDelivered    = models.NullBooleanField()

class Favourite(models.Model):
    fId            = models.AutoField(primary_key=True)
    cId            = models.ForeignKey('Customer', null=True,on_delete = models.SET_NULL)
    pId            = models.ForeignKey('Product', null = True,on_delete = models.SET_NULL) 
    class Meta:
        unique_together = (('fId', 'cId'),)


    #password  = forms.CharField(max_length=32, widget=forms.PasswordInput)


#add to basket
#    create new basket item with iscurrent set to true, if no entry with basket is current true.
#    else x
#*purchase 
#basketde isCurrent== True yoksa yeni basket objesi yaratsın
#ve sadece purchase gerçekleşirse isCurrent = False

class Invoice(models.Model):
    price = models.FloatField(null = True)
    cost  = models.FloatField(null = True)
    iId = models.AutoField(primary_key=True)
    time  = models.DateTimeField(null=True)
    

    # we should inlcude date field
    # store profit and loss information 
    class Meta:
        unique_together = (('iId', 'bId','dId','cId'),)
    cId = models.ForeignKey('Customer', null=True,on_delete = models.SET_NULL)
    bId = models.ForeignKey('Basket', null = True,on_delete = models.SET_NULL) ##### değiştirsek 
    dId = models.ForeignKey('Delivery', null = True,on_delete = models.SET_NULL)

    oId = models.ForeignKey('Order', null = True,on_delete = models.SET_NULL)
    
class Order(models.Model):
    oId = models.AutoField(primary_key=True)