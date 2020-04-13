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

class ProductManager:
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
    )
class SalesManager:
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

class Category(models.Model):
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
    iId = models.AutoField(primary_key=True)
    
    class Meta:
        unique_together = (('iId', 'bId','dId','cId'),)
    cId = models.ForeignKey('Customer', null=True,on_delete = models.SET_NULL)
    bId = models.ForeignKey('Basket', null = True,on_delete = models.SET_NULL) ##### değiştirsek 
    dId = models.ForeignKey('Delivery', null = True,on_delete = models.SET_NULL)
    

#def  deleteProduct():
#    isActive = False

#def retrieveAllProducts():
    ##filter by active == True

#def retrieveAllInvoice():

#accessdata (Invoice, filter = isActive == True )




""" Official Code Sample
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
"""


"""  Foreign Key
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
"""


""" ManyToManyField
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
"""

"""
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
"""

"""
Automatic primary key fields¶
By default, Django gives each model the following field:

id = models.AutoField(primary_key=True)
This is an auto-incrementing primary key.

If you’d like to specify a custom primary key, specify primary_key=True on one of your fields. If Django sees you’ve explicitly set Field.primary_key, it won’t add the automatic id column.

Each model requires exactly one field to have primary_key=True (either explicitly declared or automatically added).
"""



""" Composite Idea
class MyTable(models.Model):
    class Meta:
        unique_together = (('key1', 'key2'),)

    key1 = models.IntegerField()
    key2 = models.IntegerField()

    class MyTable(models.Model):
    class Meta:
        unique_together = (('key1', 'key2'),)

    key1 = models.IntegerField(primary_key=True)
    key2 = models.IntegerField()

"""

""" how to declare bollean field
active = models.NullBooleanField()
"""


### silme 1 : 
    #aktif  bir silme yok
    #product manager yapıyor
    #etkisi ne :
    #    eski faturalarda sorun yok

### silme  2 : ürüne ait her şeyi silme faturası bilgisi functional bir şey değil by force
    #admin ürünü yok istiyor
    #setNULL fatura kalıcak ama ürün yok , fiyatı yok , Cid kime sattığını biliyor , kim kaç ürün almış
    #Cascade fatura da yok


#user bought many products using delivery X

# cid =5
# dId =3


# basket 


#satın alınan ürünler
# Client ,cid =5  , products = 1,2, 4
"""
Bugun gittin 3 tane ürün aldın
Yarın da iki aldın

Basket Table ne var ?
basket id ,Client id ,product id ,

ilk gün:
    5  1 
    5  2
    5  4

ikinci gün:
    5  999
    5  888

hangisinin birinci gün hangisinin ikinci gün olduğunu nerden biliyorsun ?
"""