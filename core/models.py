from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'id':self.id, 'slug':self.slug})


class Cart(models.Model):
     created = models.DateTimeField(auto_now_add=True)

     def get_total_price(self):
         return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name = 'items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def get_total_cost(self):
        return sum(item.get_total_cost() for item in self.item.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_cost(self):
        return self.price * self.quantity