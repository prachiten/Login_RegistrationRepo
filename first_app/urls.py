from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.create_user),
    path('login',views.login),
    path('welcome',views.welcome),
    path('logout',views.logout),
]