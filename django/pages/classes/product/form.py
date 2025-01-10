from django import forms
from ...models import Product, ProductImage, ProductVideo
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'reoccurrence', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'reoccurrence': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description', 'rows': 3}),
        }
        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'image_url']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter external image URL'}),
        }

class ProductVideoForm(forms.ModelForm):
    class Meta:
        model = ProductVideo
        fields = ['video', 'video_url']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter external video URL'}),
        }