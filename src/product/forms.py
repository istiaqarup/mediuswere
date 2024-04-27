from django import forms

from product.models import Variant,Product


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'sku']
        widgets = {
            'variants': forms.CheckboxSelectMultiple(),
        }
class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['title', 'description', 'active']  # Include other fields if needed        
class ProductFilterForm(forms.Form):
    title = forms.CharField(required=False, label='Product Title', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Title'}))
    productvariant = forms.CharField(required=False, label='Variant', widget=forms.Select(attrs={'class': 'form-control'}, choices=[('--SHOW MORE--', '--SHOW MORE--')]))
    price_from = forms.DecimalField(required=False, min_value=0, label='Price From', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From'}))
    price_to = forms.DecimalField(required=False, min_value=0, label='Price To', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To'}))
    date = forms.DateField(required=False, label='Date', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date', 'type': 'date'}))