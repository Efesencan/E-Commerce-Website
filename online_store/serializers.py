
from rest_framework import serializers
from .models import Account, Product,Category,Customer,Basket,Favourite,Invoice,Delivery,Rating,Address
from django.db.models import Avg
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['fav_color'] = user.fav_color
        return token
"""
class AccountSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    age      = serializers.CharField() # front will sent us with this format
    sex      = serializers.BooleanField()


    class Meta:
        model = Account
        fields = ('email', 'username', 'password','age','sex')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        account = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            account.set_password(password)
        account.save()
        return account
    # def update() make need in future


class ProductSerializer(serializers.ModelSerializer):
    """ Product Model Serializer """

    class Meta:
        model = Product
        exclude = ['isActive','pId']


class CardSerializer(serializers.ModelSerializer):   
    # view that use this serializer:
    #search        
    avgRating = serializers.SerializerMethodField()
    """ Product Model Serializer """
    class Meta:
        model = Product
        fields = ['pId','price', 'oldPrice', 'imgSrc', 'name','stock','categoryName','avgRating','displayOldPrice']
    def get_avgRating(self,obj):
        x= (Rating.objects.filter(pId = obj.pId, waitingForApproval =False,Approved=True).aggregate(Avg('rating'))["rating__avg"])
        if x is not None:
            return int(x)
        else:
            return 0




class ProductDetailSerializer(serializers.ModelSerializer):
    # view that use this serializer:
     
    #filterProduct 
    #productDetail 
    categoryName     = serializers.CharField(source ='categoryName.categoryName')
    images           = serializers.StringRelatedField(many=True)
    
    numComment = serializers.SerializerMethodField()
    avgRating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['pId','price', 'oldPrice', 'imgSrc', 'name','stock','cost','modelNo','description','warrantyStatus','disturbuterInfo','categoryName','listedDate','images','numComment','avgRating','displayOldPrice']
    def get_numComment(self,obj):
        return len(Rating.objects.filter(pId = obj.pId))

    def get_avgRating(self,obj):
        x= (Rating.objects.filter(pId = obj.pId, waitingForApproval =False, Approved=True).aggregate(Avg('rating'))["rating__avg"])
        if x is not None:
            return int(x)
        else:
            return 0
class CategorySerializer(serializers.ModelSerializer):
    """ Product Model Serializer """
    class Meta:
        model = Category
        fields = ['categoryName',"categoryIconScr"]
        

class BasketSerializer (serializers.ModelSerializer):
    
    name             = serializers.CharField(source='pId.name')
    price            = serializers.FloatField(source='totalPrice')  
    description      = serializers.CharField(source = 'pId.description')
    imgSrc           = serializers.CharField(source='pId.imgSrc')
    modelNo          = serializers.CharField(source='pId.modelNo') # TEXT ,BV200423 universal code
    warrantyStatus   = serializers.IntegerField(source = 'pId.warrantyStatus')
    disturbuterInfo  = serializers.CharField(source= 'pId.disturbuterInfo') #TEXT
    categoryName     = serializers.CharField(source = 'pId.categoryName.categoryName')
    categoryIconScr  = serializers.CharField(source = 'pId.categoryName.categoryIconScr')
    listedDate       = serializers.DateField(source = 'pId.listedDate')

    class Meta:
        model = Basket
        fields = ['pId','isPurchased','quantity','name',
                  'price','description','imgSrc','modelNo',
                  'warrantyStatus','disturbuterInfo','categoryName','categoryIconScr',
                  'listedDate']

class FavouriteSerializer(serializers.ModelSerializer):

    name             = serializers.CharField(source='pId.name')
    price            = serializers.FloatField(source='pId.price')
    categoryName     = serializers.CharField(source ='pId.categoryName.categoryName')
    imgSrc           = serializers.CharField(source='pId.imgSrc')


    class Meta:
        model = Favourite
        fields = ['pId','name','price','categoryName','imgSrc',]

class InvoiceSerializerProductManager(serializers.ModelSerializer):

    address     =serializers.CharField(source='dId.address')
    IsDelivered = serializers.NullBooleanField(source='dId.IsDelivered')
    class Meta:
        model = Invoice
        fields = ['cId','bId','iId','time','IsDelivered','address',]

class InvoiceSerializerProductManager2(serializers.ModelSerializer):

    address     =serializers.CharField(source='dId.address')
    IsDelivered = serializers.NullBooleanField(source='dId.IsDelivered')
    productName = serializers.CharField(source='bId.pId.name')
    class Meta:
        model = Invoice
        fields = ['iId','time','IsDelivered','address','productName']

class InvoiceSerializerOrders(serializers.ModelSerializer):

    
    IsDelivered = serializers.NullBooleanField(source='dId.IsDelivered')
    name = serializers.CharField(source='bId.pId.name')
    imgSrc= serializers.CharField(source='bId.pId.imgSrc')
    pId = serializers.CharField(source='bId.pId.pId')

    class Meta:
        model = Invoice
        fields = ['time','IsDelivered','pId','name','imgSrc','price']

class InvoiceSerializerSaleManagerOrders(serializers.ModelSerializer):

    
    IsDelivered = serializers.NullBooleanField(source='dId.IsDelivered')
    name = serializers.CharField(source='bId.pId.name')
    imgSrc= serializers.CharField(source='bId.pId.imgSrc')
    pId = serializers.CharField(source='bId.pId.pId')
    profit = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['time','IsDelivered','pId','name','imgSrc','price','cost','profit']

    def get_profit(self,obj):
        return format(obj.price - obj.cost,'.2f')
    
    def get_price(self,obj):
        return format(obj.price,'.2f')

class RatingSerializer(serializers.ModelSerializer):

    commentOwner = serializers.CharField(source='cId.user.username')
    

    class Meta:
        model = Rating
        fields = ['rId','rating','commentbody','commentHeader','commentOwner']

class MyRatingSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(source='pId.name')
    class Meta:
        model = Rating
        fields = ['rId','rating','commentbody','commentHeader','waitingForApproval','Approved','productName','pId']


class ApprovalListSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(source='pId.name')
    class Meta:
        model = Rating
        fields = ['rId','rating','commentbody','commentHeader','productName']



class SeeMyAddressSerializer(serializers.ModelSerializer):
    myAddress  = serializers.StringRelatedField(many=True)
    class Meta:
        model = Customer
        fields = ['myAddress']