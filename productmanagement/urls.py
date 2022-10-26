from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('category/',views.category,name='category'),
    path('subcategory/',views.subcategory,name='subcategory'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('viewproduct/',views.viewproduct,name='viewproduct'),
    path('singleproduct/<id>',views.singleproduct,name='singleproduct'),
    path('adminproduct/',views.adminproduct,name='adminproduct'),
    path('editproduct/ <id>',views.editproduct,name='editproduct'),
    path('removeproduct/ <id>',views.removeproduct,name='removeproduct'),
    path('banner/',views.banner,name='banner'),
    path('addbanner/',views.addbanner,name='addbanner'),
    path('allcategory/',views.allcategory,name='allcategory'),
    path('disablecategory/ <id>',views.disablecategory,name='disablecategory'),
    path('deletebanner/ <id>',views.deletebanner,name='deletebanner'),
    path('filter/ <id>',views.filter,name='filter'),
    path('editoffer/ <id>',views.editoffer,name='editoffer'),
    path('deleSubcategory/ <id>',views.deleSubcategory,name='deleSubcategory'),
    path('editProOffer ,<id>',views.editProOffer,name='editProOffer'),
    path('offermanagement',views.offermanagement,name='offermanagement'),
    path('addImage/',views.addImage,name='addImage'),

   

    

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

