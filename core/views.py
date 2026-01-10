from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem
from django.views.decorators.http import require_POST
from django.http import JsonResponse
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
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
    else:
        cart = None

    if not cart:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': f'Added {product.name} to cart'
    })

def cart_detail(request):
    cart_id = request.session.get('cart_id')
    cart = None

    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)

    return render(request, 'core/cart-detail.html', {'cart': cart})


def cart_remove(request, product_id):
     cart_id = request.session.get('cart_id')
     cart = get_object_or_404(Cart, id=cart_id)
     item = get_object_or_404(CartItem, id=cart_id, cart=cart, product_id=product_id)
     item.delete()

     return redirect('cart-details')
