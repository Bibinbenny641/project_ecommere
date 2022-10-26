import imp
from moreAdmin.models import Stock
from productmanagement.models import Category, Subcategory
from django import forms

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            'image1','image2','image3','image4'
            ]
        
