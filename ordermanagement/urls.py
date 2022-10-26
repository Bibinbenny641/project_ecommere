from django.urls import path
from . import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('myorder/',views.myorder,name='myorder'),
    path('success',views.success,name='success'),
    # path('razor',views.razor,name='razor'),
    path('cancelorder/ <id>',views.cancelorder,name='cancelorder'),
    path('paypal',views.paypal,name='paypal'),
    path('payments',views.payments,name='payments'),
    path('success1',views.success1,name='success1'),
    


]