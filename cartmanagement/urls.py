from django.urls import path
from . import views
urlpatterns = [
    path('viewcart/',views.viewcart,name='viewcart'),
    path('removecart/ <id>',views.removecart,name='removecart'),
    path('dquantity/ ',views.dquantity,name='dquantity'),
    path('iquantity/ ',views.iquantity,name='iquantity'),
    path('addwishlist/<id>',views.addwishlist,name='addwishlist'),
    path('viewwishlist/',views.viewwishlist,name='viewwishlist'),
    path('removewishlist/<id>',views.removewishlist,name='removewishlist'),

    
    


]