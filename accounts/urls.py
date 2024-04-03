from django.urls import path
from accounts.views import RegisterUser, LoginUser, LogoutUser
from . import views


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]
