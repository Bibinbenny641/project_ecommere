from django.urls import path
from . import views

urlpatterns = [
    
    path('management/',views.user,name='management'),
    path('block/<id>/',views.block,name='block')
]
