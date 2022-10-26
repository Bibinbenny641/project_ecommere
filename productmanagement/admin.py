from django.contrib import admin
from distutils.command.upload import upload

from productmanagement.models import Category, Subcategory ,Stock

# Register your models here.
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Subcategory)