
from rest_framework import serializers
from .models import Account, Product,Category,Customer,Basket,Favourite

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

    class Meta:
        model = Account
        fields = ('email', 'username', 'password')
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

    """ Product Model Serializer """
    class Meta:
        model = Product
        fields = ['pId','price', 'oldPrice', 'imgSrc', 'name','stock']


class ProductDetailSerializer(serializers.ModelSerializer):
    # view that use this serializer:
     
    #filterProduct 
    #productDetail 
    categoryName     = serializers.CharField(source ='categoryName.categoryName')
    class Meta:
        model = Product
        fields = ['pId','price', 'oldPrice', 'imgSrc', 'name','stock','cost','modelNo','description','warrantyStatus','disturbuterInfo','categoryName','listedDate']
    
class CategorySerializer(serializers.ModelSerializer):
    """ Product Model Serializer """
    class Meta:
        model = Category
        fields = ['categoryName',"categoryIconScr"]
        

class BasketSerializer (serializers.ModelSerializer):
    
    name             = serializers.CharField(source='pId.name')
    price            = serializers.FloatField(source='pId.price')
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