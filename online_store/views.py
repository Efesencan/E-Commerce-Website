from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Account # added
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer #,MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json

from .models import Product
from .serializers import ProductSerializer
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

"""
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
"""