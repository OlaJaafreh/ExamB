from django.urls import path     
from . import views
urlpatterns = [
    path('', views.loginPage,name='loginPage'),	
    path('log', views.login,name='login'),	 	   
    path('register', views.register,name='register'),  
    path('shows', views.TVshows,name='TVshows'), 
    path('logout', views.logout,name='logout'),  
    path('addShow', views.addShow,name='addShow'), 
    path('shows/new', views.newShow,name='newShow'), 
    path('shows/<int:Sid>', views.details,name='details'), 
    path('shows/edit/<int:Sid>', views.edit,name='edit'),
    path('shows/editShow/<int:Sid>', views.editShow,name='editShow'),
    path('shows/delete/<int:Sid>', views.delete,name='delete'),
    path('shows/addCom/<int:Sid>', views.addCom,name='addCom'),
    path('shows/delCom/<int:Cid>/<int:Sid>', views.delCom,name='delCom'),
]