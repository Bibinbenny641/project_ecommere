from django.urls import path
from . import views

urlpatterns = [
    
    path('adminlogin/',views.admin_login,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logoutadmin',views.logout_admin,name='logoutadmin'),
    path('adminorder/',views.adminorder,name='adminorder'),
    path('orderstatus/ <id>',views.orderstatus,name='orderstatus'),
    path('cancelorderr/<id>',views.cancelorderr,name='cancelorderr'),
    path('couponmanagement',views.couponmanagement,name='couponmanagement'),
    # path('addcoupon',views.addcoupon,name='addcoupon'),
    path('salesreport',views.salesreport,name='salesreport'),
    path('deletecoupon/ <id>',views.deletecoupon,name='deletecoupon'),

]
