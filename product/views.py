from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.


def index(request):

    products = Product.objects.all()
    context = {
        'products': products  # This must be a dictionary, not a set
    }

    product_set = set(products)
    return render(request, 'index.html',context)
    # return HttpResponse('Hello World')


def newProduct(request):
    return HttpResponse('new products')

