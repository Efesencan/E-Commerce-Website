from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.AccountCreate.as_view(), name="create_user"),
    path('somecontent/', views.OnlyUserView.as_view(), name="user_access"),
    path('ProductManagerView/', views.ProductManagerView.as_view(), name="product_manager_access"),
    path('SalesManagerView/', views.SalesManagerView.as_view(), name="sales_manager_access"),
    path('CustomerView/', views.CustomerView.as_view(), name="customer_access"),
    path('hello/', views.HelloWorldView.as_view(), name='hello_world'),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',views.LoginView.as_view(),name="login"),
    path("filterProduct",views.filterProduct.as_view(),name="filter_products"),
    path("allCategories",views.allCategories.as_view(),name="all_categories"),
    path("seeBasket",views.seeBasket.as_view(),name="see_basket"),
    path("addBasket",views.addBasket.as_view(),name="add_basket"),
    path("dellBasket",views.dellBasket.as_view(),name="dell_basket"),
    path("updateBasket",views.updateBasket.as_view(),name="update_basket"),
    path("seeFavourite",views.seeFavourite.as_view(),name="see_Favourite"),
    path("addFavourite",views.addFavourite.as_view(),name="add_Favourite"),
    path("dellFavourite",views.dellFavourite.as_view(),name="dell_Favourite"),
    path("search",views.search.as_view(),name="search"),
    path("mainPage",views.mainPage.as_view(),name="mainPage"),
    path("productDetail",views.productDetail.as_view(),name="productDetail"),
    path("userDetail",views.userDetail.as_view(),name="userDetail"),
    path("createProduct",views.createProduct.as_view(),name="createProduct"),
    path("buyBasket",views.buyBasket.as_view(),name="buyBasket"),
]

