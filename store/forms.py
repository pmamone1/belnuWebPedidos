from django import forms
from store.models import Product, Variation

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'category', 'images']
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
