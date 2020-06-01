from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Account # added
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer,CardSerializer,CategorySerializer, ProductDetailSerializer #,MyTokenObtainPairSerializer
from django.core.mail import send_mail,send_mass_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json
from django.core import serializers
from .models import Product,Category,Customer,Basket,Favourite,Delivery,Invoice,Order, Rating,Address,Coupon
from .serializers import ProductSerializer, BasketSerializer, FavouriteSerializer, InvoiceSerializerProductManager, InvoiceSerializerOrders,RatingSerializer,MyRatingSerializer,ApprovalListSerializer,SeeMyAddressSerializer,InvoiceSerializerSaleManagerOrders,InvoiceSerializerProductManager2
from datetime import datetime
from django.db.models import Avg
from django.db.models import  Q


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import math

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
            data2 = serializer.validated_data["email"]

            duplicate_users = Account.objects.filter(username=data)
            duplicate_email = Account.objects.filter(email = data2)
            if(duplicate_users):
                return Response(data={"User":"already exist"}, status=status.HTTP_409_CONFLICT)
            elif(duplicate_email):
                return Response(data={"Email":"already exist"}, status=status.HTTP_409_CONFLICT)
            else:
                user = serializer.save()
                customer = Customer(user=user,  taxNumber=None)
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
            
            isCustomer       = hasattr(user, "customer")
            isProductManager = hasattr(user, "productmanager")
            isSalesManager   = hasattr(user, "salesmanager")
            print(isCustomer,isProductManager,isSalesManager)
            Tokens["isCustomer"] = isCustomer
            Tokens["isProductManager"] = isProductManager
            Tokens["isSalesManager"] = isSalesManager

            return Response(data = Tokens,status=status.HTTP_200_OK)
        else:
            response = Response({"Error":"Not valid user"}, status=status.HTTP_400_BAD_REQUEST)
            return response 
    
class OnlyUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
            return Response(data={"You : Okay"}, status=status.HTTP_200_OK)
            
            


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
            print(query_set)
            serializer = BasketSerializer(query_set,many =True)
            print(serializer)
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
        
        #print("****************")
        #print(search)
        #print("****************")

        serializer = CardSerializer(search,many =True)
        #print("****************")
        #print(serializer.data)
        #print("****************")

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
            query_set = Product.objects.filter(categoryName=category, isActive = True)[:3].values("pId","oldPrice","price","description","imgSrc","name","displayOldPrice")
            #print("************")
            #print(query_set)
            #print("************")
            json_data = list(query_set)
            #print("************")
            #print(json_data)
            #print("************")
            all_json[category]=json_data
        

        #print("-----------------")
        #print(all_json)
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
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        if hasattr(request.user, "customer"):
            #print("****************")
            #print(request.user.username)
            #print("****************")
            print("I enter inside")
            return Response(data={"username":request.user.username,"email":request.user.email
            }, status=status.HTTP_200_OK) #JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)
        #elif hasattr(request.user, "productManager"):
        else:
            print("I enter outside")
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
            #basket update
            productsToBePurchased = Basket.objects.filter(cId=request.user.customer.cId,isPurchased=False)
            print("******LIST:***********",productsToBePurchased)

            #here 
            order = Order()
            order.save()
            for productToBePurchased in productsToBePurchased:
                productToBePurchased.isPurchased = True
                delivery=Delivery(**delivery_object) 
                delivery.save()
                #if(productToBePurchased.pId.stock >= productToBePurchased.quantity ):
                #    productToBePurchased.pId.stock -=  productToBePurchased.quantity
                #    productToBePurchased.pId.save()
                #else:
                #    return Response(data= {"Not enough": "stock"},status=status.HTTP_400_BAD_REQUEST)

        
                print(productToBePurchased) 
                productToBePurchased.save()
                
                #invoice
                invoice_object = { 
                "cId"      : request.user.customer,
                "bId"      : productToBePurchased,
                "dId"      : delivery,
                "time"     : datetime.now(),
                "cost"     : productToBePurchased.pId.cost,
                "price"    : productToBePurchased.totalPrice,
                "oId"      : order,   
                }
                invoice=Invoice(**invoice_object)
                invoice.save() 

                print("Products to be purchased: **********")
                
                #allCustomerEmails(), 
            oId = order.oId
            invoices = Invoice.objects.filter(oId = oId)
        
            items = []
            totalPrice = 0
            for i in invoices:
                items.append({"price":i.price,"quantity" : i.bId.quantity,"name":i.bId.pId.name})
                totalPrice += i.price*i.bId.quantity
            print(items)

            if hasattr(request.user, "customer"): 
                username = request.user.username
                
                htmly     = get_template('email/invoiceTemplate.html')

                d = { 'username': username ,"item_list": items,"totalPrice": format(totalPrice, '.2f')}
                subject = 'New Purchase'
                from_email = 'businessdinostore@gmail.com'
                to = [ request.user.email ]
                print(to)

                message = htmly.render(d)
                
                print("**********HERE*************\n\n\n")
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                
                msg.content_subtype = 'html'

                pdfly = get_template('email/dummy.html')
                pdf = pdfly.render(d)


                outputFilename = "InvoiceTest.pdf"
                resultFile = open(outputFilename, "w+b")

                pisaStatus = pisa.CreatePDF(
                        pdf+"",                # the HTML to convert
                dest=resultFile)           # file handle to recieve result

                # # close output file
                resultFile.close() 
                msg.attach_file('InvoiceTest.pdf')  
                msg.send()
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
        data["displayOldPrice"] =True
        newProduct = Product(**data)
        newProduct.save()

     
        return Response(status=status.HTTP_200_OK)


class updateStock(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "productmanager"):
            data     = json.loads(request.body.decode('utf-8'))
            if "pId" in data:
                pId  =  data["pId"]
                stock =  data["stock"]         
                #product update
                productsToBePurchased = Product.objects.filter(pId=pId)
                productsToBePurchased_object = productsToBePurchased[0]
                productsToBePurchased_object.stock = stock
                productsToBePurchased_object.save()
                print("-------stock update-------")
            elif "name" in data:
                name  =  data["name"]
                stock =  data["stock"]         
                #product update
                productsToBePurchased = Product.objects.filter(name=name)
                productsToBePurchased_object = productsToBePurchased[0]
                productsToBePurchased_object.stock = stock
                productsToBePurchased_object.save()
            else:
                return Response(data= {"not correct api parameters you can either send name or pId with stock":"BE CAREFUL "},status=status.HTTP_400_BAD_REQUEST)
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

            #need to send notification mail here

            #customer mail
            customerMail = invoice.cId.user.email
                  
            username = invoice.cId.user.username
            items = [invoice.bId]
                
            htmly     = get_template('email/deliveryTemplate.html')

            d = { 'username': username ,"item_list": items,"isDelivered":IsDelivered}
            subject = 'Delivery Status Update'
            from_email = 'businessdinostore@gmail.com'
            to = [ customerMail]
            print(to)

            message = htmly.render(d)
            
            print("**********HERE*************\n\n\n")
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            
            msg.content_subtype = 'html'
            pdfly = get_template('email/dummy2.html')
            pdf = pdfly.render(d)


            outputFilename = "DeliveryTest.pdf"
            resultFile = open(outputFilename, "w+b")

            pisaStatus = pisa.CreatePDF(
                        pdf+"",                # the HTML to convert
                dest=resultFile)           # file handle to recieve result

                # # close output file
            resultFile.close() 
            msg.attach_file('DeliveryTest.pdf')  
        
            msg.send()

            print("-------delivery status update-------")
            return Response(status=status.HTTP_200_OK)

        else:
             Response(status=status.HTTP_400_BAD_REQUEST)

             
class orders(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if hasattr(request.user, "customer"):
            data     = json.loads(request.body.decode('utf-8'))
            

            cId = request.user.customer.cId

            Invoices = Invoice.objects.filter(cId = cId)
            if "mobile" in data:
                data = {}
                for invoice in Invoices:
                    if str(invoice.oId.oId) not in data:
                        data[str(invoice.oId.oId)] = dict ()
                        data[str(invoice.oId.oId)]["time"] = invoice.time
                        data[str(invoice.oId.oId)]["totalPrice"] = invoice.price * invoice.bId.quantity
                        data[str(invoice.oId.oId)]["items"] = [{"pId" : invoice.bId.pId.pId,"imgSrc":invoice.bId.pId.imgSrc, "quantity": invoice.bId.quantity, "price": invoice.price, "name": invoice.bId.pId.name, "isDelivered":invoice.dId.IsDelivered}]
                    else:
                        data[str(invoice.oId.oId)]["items"].append({"pId" : invoice.bId.pId.pId, "imgSrc":invoice.bId.pId.imgSrc,"quantity": invoice.bId.quantity, "price": invoice.price,"name": invoice.bId.pId.name, "isDelivered":invoice.dId.IsDelivered})
                        data[str(invoice.oId.oId)]["totalPrice"] += invoice.price * invoice.bId.quantity
                return Response(data = data , status=status.HTTP_200_OK)
            else:
                serializer = InvoiceSerializerOrders(Invoices,many =True)
                return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)
        else:
             Response(status=status.HTTP_400_BAD_REQUEST)

class deleteProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        
        if hasattr(request.user, "productmanager"):
            data = json.loads(request.body.decode('utf-8'))
            
            if "pId" in data:
                pId = data["pId"]
                
            elif "name" in data:
                name = data["name"]
                pId = Product.objects.filter(name = name)[0].pId
                #print(pId)
            else:
                return Response(data= {"not correct api parameters you can either send name or pId ":"BE CAREFUL "},status=status.HTTP_400_BAD_REQUEST)
            
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
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        #print("-----------YESSSS--------")
        if hasattr(request.user, "salesmanager"):
            """
            datetime_str = '09/19/18 13:55:26'
            datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            """
            data = json.loads(request.body.decode('utf-8'))
            #print("-------------------NOOO------")
            start = data["start"]
            end = data["end"]
            #print(start)
            #print(end)
            start = datetime.strptime(start, '%Y-%m-%d')
            end   = datetime.strptime(end,   '%Y-%m-%d')

            Invoices = Invoice.objects.filter(time__range=[start,end])
            
            serializer = InvoiceSerializerSaleManagerOrders(Invoices,many =True)
            #print(serializer.data)
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

        else:
            Response(status=status.HTTP_400_BAD_REQUEST)


def allCustomerEmails():
    allmails = [i.user.email for i in Customer.objects.all()]
    print(allmails)
    return allmails
 
class makeDiscount(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if hasattr(request.user, "salesmanager"):
           
            data = json.loads(request.body.decode('utf-8'))
            productIds = data["products"]
            discount   = data["discount"]
            body = ""
            for pId in productIds:
                product_object = Product.objects.filter(pId = pId)[0]
                product_object.price *= 1-(discount/100)
                product_object.save()
                body += product_object.name + ", "
                
                #send mail
            body = "Hello,\n" +body[:-2]  + " are in %" + str(discount) +" sale. Don't miss this opportunity."
            print(body)
            send_mail(
                'Dino',    
                body, # body şu ürün discount kadar indirime uğradı firsatı kaçırma 
                'businessdinostore@gmail.com', 
                ["gokberkyar@sabanciuniv.edu", "efesencan@sabanciuniv.edu"],
                #allCustomerEmails(), 
                fail_silently=True,
            )
            return  Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class addRating(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if hasattr(request.user, "customer"):
           
            data = json.loads(request.body.decode('utf-8'))

            rating_fields = {
            "commentHeader"      : data["commentHeader"],
            "commentbody"        : data["commentbody"],
            "rating"             : data["rating"],
            "pId"                : Product.objects.filter(pId = data["pId"])[0],  #product object
            "cId"           : request.user.customer,
            "waitingForApproval" : True,
            "Approved"           : False,
            }
            
            rating_object = Rating(**rating_fields)
            rating_object.save()
            return  Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class reviewRating(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if hasattr(request.user, "productmanager"):
            data = json.loads(request.body.decode('utf-8'))
            
            rId            = data["rId"]
            Approved       = data["approvalStatus"]
    
            rating_object = Rating.objects.filter(rId=rId)[0]
            rating_object.waitingForApproval = False
            rating_object.Approved    = Approved 
            rating_object.save()
            
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class seeRating(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        pId            = data["pId"]
        page           = data["page"] if "page" in data else None
        if page == None :

            query= Rating.objects.filter(pId = pId, waitingForApproval = False, Approved = True )
            serializer = RatingSerializer(query,many =True)
                
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)
        else:
            query= Rating.objects.filter(pId = pId, waitingForApproval = False, Approved = True )
            serializer = RatingSerializer(query,many =True)
            data = serializer.data
            elementPerPage = 8
            totalElementCount = len(data)
            lastPage = math.ceil(totalElementCount / elementPerPage)
            data= data[(page-1) * elementPerPage: page * elementPerPage]
            
            isPrevExist= True if page != 1 else False
            isNextExist= True if page < lastPage else False

            resultData  = {"data": data, "isPrevExist": isPrevExist, "isNextExist":isNextExist,"lastPage":lastPage ,"currentPage":page, "elementPerPage": elementPerPage}
            return JsonResponse(data=resultData,safe=False, status=status.HTTP_200_OK)



class deleteRating(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            rId  = data["rId"]
            Rating.objects.filter(rId=rId)[0].delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class seeMyRating(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        if hasattr(request.user, "customer"):
            
            query = Rating.objects.filter(cId = request.user.customer.cId)
            serializer = MyRatingSerializer(query,many =True)
            
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
 
class approvalList(APIView):   
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        if hasattr(request.user, "productmanager"):
            
            query = Rating.objects.filter(waitingForApproval = True)
            serializer = ApprovalListSerializer(query,many =True)
            
            return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class addAddress(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            customer_object  = request.user.customer
            address          = data["address"]
            address_object = { 
                "customer" : customer_object,
                "address"  :  address
            }
            address_object = Address(**address_object)
            address_object.save()

            
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class deleteAddress(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
                   
            Address.objects.filter(customer = request.user.customer.cId,address = data["address"])[0].delete()
                      
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class seeMyAddress(APIView,):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        if hasattr(request.user, "customer"):
            x = request.user.customer.myAddress.all()
            
            data = []
           # base = "address"
           # counter =1 
            for i in x:
                data.append({"addressId": i.aId, "address":i.address})
            #print(data)
            return Response(data = data,status=status.HTTP_200_OK)      
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class updateAddress(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            customer_object  = request.user.customer
            oldAddress          = data["oldAddress"]
            newAddress          = data["newAddress"]
         
            address_object = Address.objects.filter(customer =customer_object.cId, address=oldAddress )[0]
            address_object.address = newAddress
            address_object.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class changePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        oldPassword = data["oldPassword"]
        newPassword = data["newPassword"]
        username    = request.user.username

        user = authenticate(username=username, password=oldPassword)
        if user is not None:
            user.set_password(newPassword)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class changeEmail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        
        newEmail= data["newEmail"]
        
        duplicate_email = Account.objects.filter(email=newEmail)
        if(duplicate_email):
            return Response(data={"Email":"already exist"},status=status.HTTP_409_CONFLICT)
        else:
            request.user.email = newEmail
            request.user.save()
            return Response(status=status.HTTP_200_OK)
       


class createCoupon(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        print(request.user)
        if hasattr(request.user, "salesmanager"):
            data         = json.loads(request.body.decode('utf-8'))
            quantity     = data["quantity"] 
            couponName   = data["couponName"]
            discountRate = data["discountRate"]
            ageLow       = data["ageLow"]    if  "ageLow" in data  else 0
            ageHigh      = data["ageHigh"]   if  "ageHigh" in data else 150
            sex          = data["sex"]       if  "sex"     in data else "Both"

            sex = sex.lower()

            if sex == "both":
                accounts = Account.objects.filter(age__range= (ageLow,ageHigh),productmanager=None, salesmanager=None)
            else:
                sex = True if sex == "male" else False
                accounts = Account.objects.filter(age__range= (ageLow,ageHigh),sex = sex,productmanager=None, salesmanager=None)
           
            # accoun
            #for i in accounts:
            #    if address in i.customer.myAddress :
            #        .append(i)
            #


            count = len(accounts)
            
            for i in range(quantity):
                coupon_object = Coupon(couponName = couponName, discountRate = discountRate, cId = None)
                coupon_object.save()

            subject ="New Coupon " + couponName
            message = ["Dear " + i.username  + ", \n We have a new Coupon for you  :) " for i in accounts ]
            recipient_list= [i.email for i in accounts]
            from_email= 'businessdinostore@gmail.com'

            print("Accounts",accounts)
            print("Subject",subject)
            print("message:" , message)
            print("recicipent_list",recipient_list)
            print("from_email")
            emailList=[]
            for i in range(len(accounts)):
                emailList.append(  (subject,message[i],from_email,[recipient_list[i]])  )

            emailList= tuple(emailList)
            print(len(emailList))

            for i in emailList:
                print(i[3])
            send_mass_mail(emailList, fail_silently=False)

            
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class useCoupon(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        if hasattr(request.user, "customer"):
            data = json.loads(request.body.decode('utf-8'))
            couponName = data["couponName"]
            coupon_object = Coupon.objects.filter(couponName = couponName,cId = request.user.customer.cId)
            if len(coupon_object):
                #user used that coupon
                return Response(data={"You":"already used this coupon"},status=status.HTTP_409_CONFLICT)
            else:
                coupon_object = Coupon.objects.filter(couponName = couponName)
                if len(coupon_object):
                    coupon_object = Coupon.objects.filter(couponName = couponName,cId =None)
                    if len(coupon_object):
                    #make discount
                        customer = request.user.customer
                        coupon_object = coupon_object[0] 
                        discountRate = coupon_object.discountRate
                        basket_objects = Basket.objects.filter(cId = customer.cId, isPurchased= False)
                        for basket in basket_objects:
                            basket.totalPrice *=  1-(discountRate/100)
                            basket.totalPrice = format(basket.totalPrice, '.2f')
                            basket.save()
                        coupon_object.cId = customer
                        coupon_object.save()
                    else:
                        #all coupons used
                        return Response(data={"UNFORTUNATELY": "ALL COUPONS WERE USED"},status=status.HTTP_428_PRECONDITION_REQUIRED)
                else:
                     return Response(data={"There":"does not exist such coupon"},status=status.HTTP_404_NOT_FOUND)
               
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class navbarGlobals(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        if hasattr(request.user, "customer"):
            customer = request.user.customer
            cId = customer.cId
            countBasket = 0
            numBasket = Basket.objects.filter(cId = cId, isPurchased = False)
            for i in numBasket:
                countBasket += i.quantity
            numFav = len(Favourite.objects.filter(cId = cId))
            data = {"numBasket" : countBasket , "numFav": numFav}
            
            return Response(data = data,status=status.HTTP_200_OK)
        data = {"numBasket" : 0 , "numFav": 0}
        return Response(data = data,status=status.HTTP_200_OK)

class searchUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        
        data    = json.loads(request.body.decode('utf-8'))
        username    = data["username"]
        cId =Account.objects.filter(username=username)[0].customer.cId

        
        if hasattr(request.user, "productmanager"):               
            ratings =    Rating.objects.filter(cId = cId,waitingForApproval =True)
            ratingSerializer = ApprovalListSerializer(ratings,many =True)
            
            
          
            delivery =   Invoice.objects.filter(cId = cId ,dId__IsDelivered=False)

            invoiceSerializer = InvoiceSerializerProductManager2(delivery,many =True)
            data = {"rating": ratingSerializer.data ,"invoice":invoiceSerializer.data}
            #comment
            #delivery   
            
            return Response(data = data,status=status.HTTP_200_OK)
            


        elif hasattr(request.user, "salesmanager"):
            invoices = Invoice.objects.filter(cId = cId )
            invoiceSerializer = InvoiceSerializerSaleManagerOrders(invoices,many =True)
            data = {"invoice":invoiceSerializer.data}
            return Response(data = data,status=status.HTTP_200_OK)
            

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class advanceSearch(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        
        data    = json.loads(request.body.decode('utf-8'))
        # condition_if_true if condition else condition_if_false
        priceLow   = data["priceLow"]  if "priceLow"   in data else 0
        priceHigh  = data["priceHigh"] if "priceHigh"  in data else 9999999
        category   = data["category"]  if "category"   in data else "all"
        rating     = data["rating"]    if "rating"     in data else 0
        orderBy    = data["orderBy"]   if "orderBy"    in data else "name"
        option     = data["option"]    if "option"     in data else True
        text       = data["text"] 
        

       
        orderBy    = "productRating"   if orderBy =="rating"  else orderBy
        print("-----")
        #print(orderBy)
        #print(option)

        if text != "___category___":
            search1 = Product.objects.filter(isActive = True ,name__icontains = text)
            search2 = Product.objects.filter(isActive = True ,description__icontains = text)
            search3 = Product.objects.filter(isActive = True ,disturbuterInfo__icontains = text)
            search4 = Product.objects.filter(isActive = True ,modelNo__icontains = text)
            search5 = Product.objects.filter(isActive = True ,categoryName__categoryName__icontains = text)
            
            search = search1|search2|search3|search4|search5
        else:
            search =Product.objects.filter(isActive = True )
        query_set = search.filter(price__range=(priceLow,priceHigh))
        query_set = query_set.annotate(productAvgRating = Avg('productRating__rating',filter = Q(productRating__Approved=True )))

        if rating != 0:
            query_set  = query_set.filter(productAvgRating__gte = rating)

        if category != "all":
            query_set=query_set.filter(categoryName=category)
        
        query_set=query_set.order_by(orderBy)

        if option == False:
            query_set = query_set.reverse()
        #print(query_set)
        serializer = ProductDetailSerializer(query_set,many =True)
        return JsonResponse(data=serializer.data,safe=False, status=status.HTTP_200_OK)


class emailMyInvoice(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        
        data    = json.loads(request.body.decode('utf-8'))
        oId = data["oId"] 
        invoices = Invoice.objects.filter(oId = oId)
    
        items = []
        totalPrice = 0
        for i in invoices:
            items.append({"price":i.price,"quantity" : i.bId.quantity,"name":i.bId.pId.name})
            totalPrice += i.price * i.bId.quantity
        print(items)

        if hasattr(request.user, "customer"): 
            username = request.user.username
            
            htmly     = get_template('email/invoiceTemplate.html')

            d = { 'username': username ,"item_list": items,"totalPrice": format(totalPrice, '.2f')}
            subject = 'Invoice'
            from_email = 'businessdinostore@gmail.com'
            to = [ request.user.email ]
            print(to)

            message = htmly.render(d)
             
            print("**********HERE*************\n\n\n")
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            
            msg.content_subtype = 'html'
    
            # outputFilename = "InvoiceTest.pdf"
            # resultFile = open(outputFilename, "w+b")

            # pisaStatus = pisa.CreatePDF(
            #         message+"",                # the HTML to convert
            # dest=resultFile)           # file handle to recieve result

            # # close output file
            # resultFile.close() 
            # msg.attach_file('InvoiceTest.pdf')  
            msg.send()
                    
            return Response(status=status.HTTP_200_OK)

            

class  editProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    
    def post(self,request):
        if hasattr(request.user, "productmanager"):
            data = json.loads(request.body.decode('utf-8'))
            pId = data["pId"]
            productObject = Product.objects.filter(pId = pId)[0]
            name = data["name"]
            description  = data["desc"]
            price = data["price"]
            warranty = data["warranty"]
            modelNo = data["modelno"]
            disturbuterInfo = data["distrubutor"]
            if name != "":
                productObject.name = name
            if description != "":
                productObject.description  = desc
            if price != "":
                productObject.price = price
            if warranty != "":
                productObject.warranty = warranty
            if modelNo != "":
                productObject.modelNo = modelNo
            if disturbuterInfo != "":
                productObject.disturbuterInfo = disturbuterInfo
            productObject.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        #pId, name,desc, price,warranty,quantity,modelno,distrubutor
        
        
        
       
        