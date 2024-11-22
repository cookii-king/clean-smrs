from django.shortcuts import render

from .models import Product

def catalog(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, 'catalog.html', {'products': products})