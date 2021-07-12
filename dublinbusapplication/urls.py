from django.urls import path
from . import views
from .views import *
import dublinbusapplication

urlpatterns = [
    path('', index, name="home"),
    path('about/', views.about),
    path('contact/', views.contact),
    path('search_test/', views.search_test),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('predict/', predict, name='predict'),
]
