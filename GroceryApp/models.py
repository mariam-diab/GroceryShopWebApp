from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    # cid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet= "abcdefgh12345", prefix="cat")
    title = models.CharField(max_length=100, blank=True, null=True)
    img = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'groceryapp_category'
        verbose_name_plural = "categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.img))
    
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
    PRODUCT_UNITS = [
        ('PIECE', 'piece'),
        ('PACK', 'Pack'),
        ('KG', 'Kilogram'),
        ('SLICE', 'Slice'),
        ('BOTTLE', 'Bottle'),
        ('CAN', 'Can'),
    ]
    # pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet= "abcdefgh12345")
    # status = models.BooleanField(default= True)
    # digital = models.BooleanField(default= True)
    # updated = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete= models.SET_NULL, to_field='id', null=True)
    title = models.CharField(max_length=255)
    product_description = models.TextField(max_length=400 , blank=True, null=True, default= 'Freshly sourced from our brand selection.')
    img = models.URLField(blank=True, null=True)
    brand_name = models.CharField(max_length=100, null=False, default= 'Ogani')
    brand_nationality = models.CharField(max_length=100, null=False, default= 'Egypt')
    unit_type = models.CharField(max_length=6, choices=PRODUCT_UNITS, default='PIECE')
    unit_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2, default= 1.99)
    old_price = models.DecimalField(max_digits=20, decimal_places=2, default= 2.99)
    available_quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default= False)
    featured = models.BooleanField(default= True)
    product_status = models.CharField(choices = STATUS, max_length=10, default= 'published')
    added_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    sku = ShortUUIDField(unique=True, length=10, max_length=20, alphabet= "abcdefgh12345", prefix= "sku")
    date = models.DateTimeField(auto_now_add = True)
    exp_date = models.DateTimeField(null = True)


    class Meta:
        db_table = 'groceryapp_product'
        verbose_name_plural = 'Products'


    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.img))
    
    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price- self.price)/ self.old_price) * 100
        return new_price
    
    def save(self, *args, **kwargs):
        self.in_stock = self.available_quantity > 0
        super().save(*args, **kwargs)

    
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING ,null=True)
    images = models.URLField(null= True, blank= True)
    date = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name_plural = "Product Images"
        db_table = 'groceryapp_productimages'

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

class CartOrder(models.Model):
    ct_ord_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=False, null=False)
    # total_price = models.DecimalField(max_digits=14, decimal_places=2, default='0.00', null=True)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=30, default='Processing', choices=STATUS_CHOICE)

    class Meta:
        # managed = True
        db_table = 'groceryapp_cartorder'
        verbose_name_plural = 'Cart Order'


class CartOrderItems(models.Model):
    ct_ord_it_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(CartOrder, models.CASCADE, blank=False, null=False)
    invoice_number = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345", null = True)
    product_status = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(Product, models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='cart_order_item_images/', null=True, blank=True)


    class Meta:
            # managed = True
            db_table = 'groceryapp_cartorderitems'
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


# class Wishlist(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(User, models.CASCADE, blank=False, null=False)
#     product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

#     class Meta:
#         # managed = True
#         db_table = 'groceryapp_wishlist'
#         verbose_name_plural = 'Wishlist'

#     def __str__(self):
#         return self.product.title


class BillingDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(CartOrder, models.SET_NULL, blank=False, null=True)
    first_name = models.CharField(max_length=23)
    last_name = models.CharField(max_length=23)
    address = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100, blank=False, null=True)
    governorate = models.CharField(max_length=100, blank=False, null=True)
    city = models.CharField(max_length=100, blank=False, null=True)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=False, null=True)
    email = models.CharField(max_length=100, blank=False, null=True)
    payment_method = models.CharField(max_length=50, blank=False, null=True)
    payment_status = models.BooleanField(blank=False, null=False)
    to_be_paid = models.DecimalField(max_digits=20, decimal_places=2, default= 0)
    delivered_status = models.BooleanField(default=False)

    class Meta:
        # managed = True
        db_table = 'groceryapp_billingdetails'
        verbose_name_plural = 'Billing Details'

# class ProductReviews(models.Model):
#     user = models.ForeignKey(User, models.SET_NULL, blank=False, null=True)
#     product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
#     rating = models.IntegerField(choices= RATING, default= None)
#     date = models.DateTimeField(auto_now_add= True)

#     class Meta:
#         db_table = 'groceryapp_productreviews'
#         verbose_name_plural = "Product Reviews"
    
#     def __str__(self):
#         return self.product.title

#     def get_rating(self):
#         return self.rating
