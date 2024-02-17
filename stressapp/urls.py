from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('signout/', views.signout, name="signout"),
    path('homepage/', include("homepage.urls"), name="homepage"),
]
