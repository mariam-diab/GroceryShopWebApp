from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField

# Create your models here.

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet= "abcdefgh12345", prefix="cat")
    title = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=True, null=True)
    img = models.ImageField(blank=True, null=True, upload_to= 'category')

    class Meta:
        verbose_name_plural = "categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.img.url))
    
    def __str__(self):
        return self.title
    
STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)
STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', "published"),
)
RATING = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)



class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet= "abcdefgh12345")

    category = models.ForeignKey(Category, on_delete= models.SET_NULL, to_field='cid', blank=True, null=True)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    

    title = models.CharField(max_length=100)
    img = models.ImageField(blank=True, null=True, upload_to= 'user_directory_path')

    p_description = models.TextField(blank=True, null=True, default= 'This is the product')

    price = models.DecimalField(max_digits=20, decimal_places=2, default= 1.99)
    old_price = models.DecimalField(max_digits=20, decimal_places=2, default= 2.99)

    specifications = models.TextField(blank=True, null=True) 

    product_status = models.CharField(choices = STATUS, max_length=10, default= 'in_review')

    status = models.BooleanField(default= True)
    in_stock = models.BooleanField(default= True)
    featured = models.BooleanField(default= True)
    digital = models.BooleanField(default= True)

    sku = ShortUUIDField(unique=True, length=10, max_length=20, alphabet= "abcdefgh12345", prefix= "sku")

    date = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.img.url))
    
    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price- self.price)/ self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING ,null=True)
    images = models.ImageField(upload_to='product-images')
    date = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name_plural = "Product Images"

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)
class CartOrder(models.Model):
    ct_ord_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=False, null=False)
    price = models.DecimalField(max_digits=14, decimal_places=2, default='0.99', null=True)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=30, db_collation='Arabic_CI_AI', default='Processing', choices=STATUS_CHOICE)

    class Meta:
        # managed = True
        # db_table = 'groceryapp_cartorder'
        verbose_name_plural = 'Cart Order'


class CartOrderItems(models.Model):
    ct_ord_it_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(CartOrder, models.CASCADE, blank=False, null=False)
    invoice_number = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345", null = True)
    product_status = models.CharField(max_length=200, db_collation='Arabic_CI_AI', blank=True, null=True)
    product = models.ForeignKey(Product, models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='cart_order_item_images/', null=True, blank=True)


    class Meta:
            # managed = True
            # db_table = 'groceryapp_cartorderitems'
            verbose_name_plural = 'Cart Order Items'

    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price
            self.image = self.product.img
            self.product_status = self.product.product_status
        else:
            self.price = 0.0
            self.image = None

        self.total = self.price * self.quantity

        super(CartOrderItems, self).save(*args, **kwargs)
    

        def order_image(self):
            return mark_safe('<img src="/media/%s" width="50" height="50" />' %(self.image))


class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        # managed = True
        # db_table = 'groceryapp_wishlist'
        verbose_name_plural = 'Wishlist'

    def __str__(self):
        return self.product.title


class BillingDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(CartOrder, models.SET_NULL, blank=False, null=True)
    first_name = models.CharField(max_length=23)
    last_name = models.CharField(max_length=23)
    address = models.CharField(max_length=100, db_collation='Arabic_CI_AI')
    apartment = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=False, null=True)
    governorate = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=False, null=True)
    city = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=False, null=True)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, db_collation='Arabic_CI_AI', blank=False, null=True)
    email = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=False, null=True)
    payment_method = models.CharField(max_length=50, db_collation='Arabic_CI_AI', blank=False, null=True)
    payment_status = models.BooleanField(blank=False, null=False)
    to_be_paid = models.DecimalField(max_digits=20, decimal_places=2, default= 0)
    delivered_status = models.BooleanField(default=False)

    class Meta:
        # managed = True
        # db_table = 'GroceryApp_BillingDetails'
        verbose_name_plural = 'Billing Details'

class ProductReviews(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=False, null=True)
    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    rating = models.IntegerField(choices= RATING, default= None)
    date = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating
