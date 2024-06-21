from django.urls import path     
from . import views
urlpatterns = [
    path('', views.loginPage,name='loginPage'),	
    path('log', views.login,name='login'),	 	   
    path('register', views.register,name='register'),   
]