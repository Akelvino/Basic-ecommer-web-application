from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available = True)
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.filter(category=category)
    
    return render(request, 'core/list.html',{
        'category':category,
        'products':products,
        'categories':categories
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'core/detail.html', {'product':product})