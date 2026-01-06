from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Cart, CartItem
from django.views.decorators.http import require_POST

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available = True)
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=category)
    
    return render(request, 'core/list.html',{
        'category':category,
        'products':products,
        'categories':categories
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'core/detail.html', {'product':product})

@require_POST
def cart_add(request, product_id):
    cart_id = request.session.get('card_id')

    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart_id

        product = get_object_or_404(Product, id=product_id)

        cart_item , created = CartItem.objects.create(cart=cart, product=product)

    if not created:
        cart_item.quality +=1
    
    cart_item.save()

    responce_data ={
        'success':True,
        'message':f"Added {product.name} to cart"
    }

def cart_detail(request):
     cart_id = request.session.get('card_id')
     cart = None
     if cart_id:
         cart = get_object_or_404(Cart, id=cart_id)
         
     return render(request, 'core/cart-detail.html')