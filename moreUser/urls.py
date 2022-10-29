from django.urls import path
from . import views

urlpatterns = [
    path('userlogin/',views.user_login,name='userlogin'),
    path('',views.home,name='home'),
    path('usersignup/',views.usersignup,name='usersignup'),
    path('logout',views.logout_user,name='logoutuser'),
    path('otp/ ',views.otp,name='otp'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('address/',views.address,name='address'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('deleteaddress/<id>',views.deleteaddress,name='deleteaddress'),
    path('otplogin',views.otplogin,name='otplogin'),
    path('otp1/ ',views.otp1,name='otp1'),




   
    
]
