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
    ("process", "Processing"),
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
        new_price = (self.price/ self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING ,null=True)
    images = models.ImageField(upload_to='product-images')
    date = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name_plural = "Product Images"
