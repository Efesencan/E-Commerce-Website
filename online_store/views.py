from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Account # added
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer,CardSerializer,CategorySerializer #,MyTokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json
from django.core import serializers
from .models import Product,Category,Customer,Basket
from .serializers import ProductSerializer, BasketSerializer
from datetime import datetime
"""class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
"""


def index(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set,many =True)
    return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AccountCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data["username"]
            duplicate_users = Account.objects.filter(username=data)
            if(duplicate_users):
                return Response(data={"User":"already exist"}, status=status.HTTP_409_CONFLICT)
            else:
                user = serializer.save()
                customer = Customer(user=user, address=None, taxNumber=None)
                print("aaa")
                print(customer)
                customer.save()

                if user:
                    Tokens = get_tokens_for_user(user)
                    return Response(data=Tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HelloWorldView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if request.user.isProductManager:
            print("AAAAAA----",request.user.isCustomer)
            print("AAAAAA----",request.user.isProductManager)
            return Response(data={"hello":"world"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Your are not a Product Manager"}, status=status.HTTP_200_OK)
    
class LoginView(APIView):   

    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            Tokens = get_tokens_for_user(user)
            return Response(data = Tokens,status=status.HTTP_200_OK)
        else:
            response = Response({"Error":"Not valid user"}, status=status.HTTP_400_BAD_REQUEST)
            return response 
    
class OnlyUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
            return Response(data={"You : Okay"}, status=status.HTTP_200_OK)
            
class CustomerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if request.user.isCustomer:           
             return Response(data={"You are  : Customer"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Your are not : Customer"}, status=status.HTTP_400_BAD_REQUEST)
class ProductManagerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if request.user.isProductManager:           
            return Response(data={"You are  : ProductManager"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Your are not : ProductManager"}, status=status.HTTP_400_BAD_REQUEST)


class SalesManagerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if request.user.isSalesManager:           
            return Response(data={"Your are  : SaleManager"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Your are not : SaleManager"}, status=status.HTTP_400_BAD_REQUEST)
            


class allProducts(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        print( "Request: ------" ,request.GET.get("count"))

        count = request.GET.get("count")
        order_with = request.GET.get("order_with")
        option = request.GET.get("option")
        theCategory = request.GET.get("categoryName")

        filters = {"isActive": True}
        if theCategory != None :
            filters["categoryName"] = theCategory
    
        query_set = Product.objects.filter( **filters ).order_by( order_with if order_with != None else "name" )
        
        
        if option == "False":
            query_set = query_set.reverse()

        query_set = query_set[:int(count) if count != None else 5]



        #query_set = Product.objects.all()
        serializer = CardSerializer(query_set,many =True)
        return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)



class allCategories(APIView ):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
       
        query_set = Category.objects.all()
        serializer = CategorySerializer(query_set,many =True)
        return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

class  seeBasket (APIView ):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if hasattr(request.user, "customer"):
            filters = {
                    "cId":request.user.customer.cId,
                    "isPurchased": False,
                    }
            
            query_set = Basket.objects.filter( **filters )
            serializer = BasketSerializer(query_set,many =True)
           
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)


 

class addBasket(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
         if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            basket_object = { 
            "quantity"      : data["quantity"],
            "totalPrice"    : data["totalPrice"],
            "pId"           : Product.objects.get(pId=data["pId"]),
            "cId"           : request.user.customer,
            "purchasedDate" : datetime.now(),             #NOW
            "isPurchased"   : False
            }
            check_pId = Basket.objects.filter(pId=data["pId"] ,cId=request.user.customer.cId,isPurchased=False)
            if  len(check_pId) == 0:
                basket=Basket(**basket_object) 
                basket.save()
            else:
                check_pId[0].quantity += data["quantity"]
                check_pId[0].save()
           
            return Response(status=status.HTTP_200_OK)

class dellBasket(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
         if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            pId = data["pId"]
            cId = request.user.customer.cId
            Basket.objects.filter(pId=pId, cId = cId,isPurchased=False).delete()
            
            return Response(status=status.HTTP_200_OK)


class updateBasket(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
         if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            pId = data["pId"]
            quantity = data["quantity"]
            print(data["quantity"])
            cId = request.user.customer.cId
            basket_object_list = Basket.objects.filter(pId=data["pId"] ,cId=request.user.customer.cId,isPurchased=False)
            print(basket_object_list)
            basket_object = basket_object_list[0] # it has one element always
            print(basket_object)
            basket_object.quantity = data["quantity"]
            basket_object.save()
            
            return Response(status=status.HTTP_200_OK)


