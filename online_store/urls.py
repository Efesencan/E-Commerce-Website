from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/create/', views.AccountCreate.as_view(), name="create_user"),
    path('hello/', views.HelloWorldView.as_view(), name='hello_world'),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

#{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NjE3MjgwNCwianRpIjoiYzRhNTg0NWUxNTA4NGY2ZDhhOGFjMGU0M2FhNDMyNDAiLCJ1c2VyX2lkIjoxfQ.3bNjChP0FvjohUCY7t9abfXyMpcn3y-tVWygbIkDAvA",
#"access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0OTYzNTA0LCJqdGkiOiIyNDFlNDkxYjIzMzM0MjU0YTMzYmFlNWI4NDNmMjk1NyIsInVzZXJfaWQiOjF9.TZPF5yRZK2fM20W3FwwWxI8uOTLnJXRhcxA8m5IbXgw"}

{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NjE3Njg3NCwianRpIjoiYWM1ZTRhZDkwODVmNDhjZTk1YmRmZTA2OGJhMjIyMmMiLCJ1c2VyX2lkIjoyfQ.PPyJst279jfw2erUWEdF2TtdIbwegnLYLuOtRauNrP4",
"access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0OTY3NTc0LCJqdGkiOiJjNGVmMmM4ZjJlNGE0N2E4YTJhMTVkODVlNGQ0NjM0NiIsInVzZXJfaWQiOjJ9.579ZoZSjRPkfxPUi3wFjWMyv86qhawHCD5bvFiTa9xo"}