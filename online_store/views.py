from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Account # added
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer,CardSerializer,CategorySerializer, ProductDetailSerializer #,MyTokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json
from django.core import serializers
from .models import Product,Category,Customer,Basket,Favourite,Delivery,Invoice
from .serializers import ProductSerializer, BasketSerializer, FavouriteSerializer, InvoiceSerializerProductManager, InvoiceSerializerOrders
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


    
class LoginView(APIView):   

    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            Tokens = get_tokens_for_user(user)
            isCustomer = hasattr(request.user, "customer")
            isProductManager = hasattr(request.user, "productmanager")
            isSalesManager = hasattr(request.user, "salemanager")
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
            


class filterProduct(APIView):
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
        serializer = ProductDetailSerializer(query_set,many =True)
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


class addFavourite(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
         if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            pId = Product.objects.get(pId=data["pId"])
            cId = request.user.customer
            favourite_object_list = Favourite.objects.filter(pId=data["pId"] ,cId=request.user.customer.cId)
            if(len(favourite_object_list) == 0):
                new_fav=Favourite(pId=pId ,cId=cId)
                new_fav.save()
            
            return Response(status=status.HTTP_200_OK)
            


class dellFavourite(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
         if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            pId = data["pId"]
            cId = request.user.customer.cId

            Favourite.objects.filter(pId=pId, cId = cId).delete()
            
            return Response(status=status.HTTP_200_OK)
            
class  seeFavourite(APIView ):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if hasattr(request.user, "customer"):
            filters = {
                    "cId":request.user.customer.cId,
                    }
            
            query_set = Favourite.objects.filter( **filters )
            serializer = FavouriteSerializer(query_set,many =True)
           
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)



class search(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        
        data    = json.loads(request.body.decode('utf-8'))
        text    = data["text"]
        search1 = Product.objects.filter(isActive = True ,name__icontains = text)
        search2 = Product.objects.filter(isActive = True ,description__icontains = text)
        search3 = Product.objects.filter(isActive = True ,disturbuterInfo__icontains = text)
        search4 = Product.objects.filter(isActive = True ,modelNo__icontains = text)
        search5 = Product.objects.filter(isActive = True ,categoryName__categoryName__icontains = text)
        
        search = search1|search2|search3|search4|search5
        
        print("****************")
        print(search)
        print("****************")

        serializer = CardSerializer(search,many =True)
        print("****************")
        print(serializer.data)
        print("****************")

        return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

class mainPage(APIView):

    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        
        # filters = {
        #         "cId":request.user.customer.cId,
        #         "isPurchased": False,
        #         }


        #how to get all category names
        categoryObjects = Category.objects.all().values("categoryName")
        categories = [ i["categoryName"] for i in categoryObjects]
        all_json = {}
        item = 0
        for category in categories:
            query_set = Product.objects.filter(categoryName=category, isActive = True)[:8].values("pId","oldPrice","price","description","imgSrc","name")
            print("************")
            print(query_set)
            print("************")
            json_data = list(query_set)
            print("************")
            print(json_data)
            print("************")
            all_json[category]=json_data
        

        print("-----------------")
        print(all_json)
        # merge all the json at the end  
        # send the json to thre front
        return JsonResponse(data=all_json,safe=False, status=status.HTTP_200_OK)


class productDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        pId = request.GET.get("pId")
        query_set = Product.objects.filter(pId = pId)
        serializer = ProductDetailSerializer(query_set,many =True)
        return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

class userDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        if hasattr(request.user, "customer"):
            print("****************")
            print(request.user.username)
            print("****************")
            return Response(data={"username":request.user.customer.username,
            "user_address" :  request.user.address
                                     }, status=status.HTTP_200_OK) #JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)
        #elif hasattr(request.user, "productManager"):
        else:
            return Response(data={"Not":Customer}, status=status.HTTP_400_BAD_REQUEST)




class buyBasket(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "customer"):
            data     = json.loads(request.body.decode('utf-8'))
            address  =  data["address"]
            #user address update !
            request.user.customer.address = address
            request.user.customer.save()
            
            #delivery
            delivery_object = { 
            "address"      : address,
            "IsDelivered"    : False,
            }
            delivery=Delivery(**delivery_object) 
            delivery.save()
            
            #basket update
            productsToBePurchased = Basket.objects.filter(cId=request.user.customer.cId,isPurchased=False)
            print("******LIST:***********",productsToBePurchased)
            for productToBePurchased in productsToBePurchased:
                productToBePurchased.isPurchased = True
                print(productToBePurchased) 
                productToBePurchased.save()
                #invoice
                invoice_object = { 
                "cId"      : request.user.customer,
                "bId"      : productToBePurchased,
                "dId"      : delivery,
                "time"     : datetime.now(),
                "cost"     : productToBePurchased.pId.cost,
                "price"    : productToBePurchased.pId.price,   
                }
                invoice=Invoice(**invoice_object)
                invoice.save() 

                print("Products to be purchased: **********")
               
                print("**********")

        return Response(status=status.HTTP_200_OK)

class createProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        categoryName = Category.objects.filter(categoryName =data["categoryName"])

        if(len(Product.objects.filter(name=data["name"]))):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if (len(categoryName)) == 1: #if category exist
            data["categoryName"] = categoryName[0]
            
        else: #new category
            categoryIconScr = data["categoryIconScr"]
            newCategory = Category(categoryName = data["categoryName"], categoryIconScr =categoryIconScr)
            newCategory = newCategory.save()
            data["categoryName"] =newCategory
        del data["categoryIconScr"]
        data["isActive"] = True
        newProduct = Product(**data)
        newProduct.save()

     
        return Response(status=status.HTTP_200_OK)


class updateStock(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "productmanager"):
            data     = json.loads(request.body.decode('utf-8'))
            pId  =  data["pId"]
            stock =  data["stock"]         
            #product update
            productsToBePurchased = Product.objects.filter(pId=pId)
            productsToBePurchased_object = productsToBePurchased[0]
            productsToBePurchased_object.stock = stock
            productsToBePurchased_object.save()
            print("-------stock update-------")
            return Response(status=status.HTTP_200_OK)

        else:
             Response(status=status.HTTP_400_BAD_REQUEST)

class seeInvoiceProductManager(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        if hasattr(request.user, "productmanager"):

            Invoices = Invoice.objects.all()
            
            serializer = InvoiceSerializerProductManager(Invoices,many =True)
           
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

        else:
             Response(status=status.HTTP_400_BAD_REQUEST)


class updateDelivery(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "productmanager"):
            data     = json.loads(request.body.decode('utf-8'))
            iId  =  data["iId"]
            deliveryStatus =  data["deliveryStatus"]         
            #product update
            InvoiceList= Invoice.objects.filter(iId=iId)
            invoice  = InvoiceList[0]
            delivery_object= invoice.dId
            
            IsDelivered = True   if  deliveryStatus == "True" else False
            delivery_object.IsDelivered =  IsDelivered
            delivery_object.save()

           
            print("-------delivery status update-------")
            return Response(status=status.HTTP_200_OK)

        else:
             Response(status=status.HTTP_400_BAD_REQUEST)

             
class orders(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        if hasattr(request.user, "customer"):

            cId = request.user.customer.cId

            Invoices = Invoice.objects.filter(cId = cId)

            serializer = InvoiceSerializerOrders(Invoices,many =True)
           
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

        else:
             Response(status=status.HTTP_400_BAD_REQUEST)

class deleteProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
        if hasattr(request.user, "productmanager"):
            data = json.loads(request.body.decode('utf-8'))
            pId = data["pId"]
            
            Basket.objects.filter(isPurchased=False , pId = pId).delete()
            Favourite.objects.filter(pId=pId).delete()
            product = Product.objects.filter(pId=pId)[0]
            product.isActive = False
            product.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class addCategory(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "productmanager"):
            data = json.loads(request.body.decode('utf-8'))
            category_object = { 
            "categoryName"      : data["categoryName"],
            "imgSrc"            : data["imgSrc"],
            }

            
            if  len(Category.objects.filter(categoryName = data["categoryName"] )) == 0:
                category_object=Category(**category_object) 
                category_object.save()
            
           
        return Response(status=status.HTTP_200_OK)

class invoiceGivenRange(APIView):
    pass 

