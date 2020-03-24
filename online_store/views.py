from django.shortcuts import render
from django.http import HttpResponse
from .models import Account # added
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer #,MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
"""class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
"""


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
                return Response(data={"User":"already exist"}, status=status.HTTP_200_OK)
            else:
                user = serializer.save()
                if user:
                    json = serializer.data
                    return Response(json, status=status.HTTP_201_CREATED)
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
    def get(self, request):
        form = AuthenticationForm()
        return render(request,"registration/login.html",{"form":form})
        
    def post(self,request):
        form = AuthenticationForm(data = request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            Tokens = get_tokens_for_user(user)
            return Response(data = Tokens,status=status.HTTP_200_OK)
        else:
            return Response({"Not":"Care"}, status=status.HTTP_400_BAD_REQUEST)
    

class CustomerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if request.user.isCustomer:           
            return render(request,"customer/customer.html")
        else:
            return Response(data={"Your are not : Customer"}, status=status.HTTP_200_OK)



"""
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
"""