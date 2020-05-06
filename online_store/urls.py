from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.AccountCreate.as_view(), name="create_user"),
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
    path("buyBasket",views.buyBasket.as_view(),name="buyBasket"),

    path("createProduct",views.createProduct.as_view(),name="createProduct"),
    path("updateStock",views.updateStock.as_view(),name="updateStock"),
    path("seeInvoiceProductManager",views.seeInvoiceProductManager.as_view(),name="seeInvoiceProductManager"),
    path("updateDelivery",views.updateDelivery.as_view(),name="updateDelivery"),
    path("orders",views.orders.as_view(),name="orders"),
    path("deleteProduct",views.deleteProduct.as_view(),name="deleteProduct"),
    path("invoiceGivenRange",views.invoiceGivenRange.as_view(),name="invoiceGivenRange"),
    path("addCategory",views.addCategory.as_view(),name="addCategory"),
    path("makeDiscount",views.makeDiscount.as_view(),name="makeDiscount"),
    path("addRating",views.addRating.as_view(),name="addRating"),
    path("reviewRating",views.reviewRating.as_view(),name="reviewRating"),
    path("seeRating",views.seeRating.as_view(),name="seeRating"),
    path("deleteRating",views.deleteRating.as_view(),name="deleteRating"),
    path("seeMyRating",views.seeMyRating.as_view(),name="seeMyRating"),
    path("approvalList",views.approvalList.as_view(),name="approvalList"),
    path("addAddress",views.addAddress.as_view(),name="addAddress"),
    path("deleteAddress",views.deleteAddress.as_view(),name="deleteAddress"),
    path("seeMyAddress",views.seeMyAddress.as_view(),name="seeMyAddress"),
    path("updateAddress",views.updateAddress.as_view(),name="updateAddress"),
    path("changePassword",views.changePassword.as_view(),name="changePassword"),
    path("changeEmail",views.changeEmail.as_view(),name="changeEmail"),
    path("createCoupon",views.createCoupon.as_view(),name="createCoupon"),
    path("useCoupon",views.useCoupon.as_view(),name="useCoupon"),
    path("navbarGlobals",views.navbarGlobals.as_view(),name="navbarGlobals"),
    path("searchUser",views.searchUser.as_view(),name="searchUser"),
]



