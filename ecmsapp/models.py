from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Shop_Owner(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=128,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=128,null=True)
    prfile_pic = models.ImageField(default="profile1.png",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=128,null=True)
    phone = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=128,null=True)
    profile_pic = models.ImageField(default="profile1.png",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product_Tag(models.Model):
    product_tag = models.CharField(max_length=128,null=True)

    def __str__(self):
        return self.product_tag

class Shop_Tag(models.Model):
    shop_tag = models.CharField(max_length=128,null=True)

    def __str__(self):
        return self.shop_tag

class Shop(models.Model):
    shop_owner = models.ForeignKey(Shop_Owner,null=True,on_delete = models.CASCADE)
    shop_name = models.CharField(max_length=128,null=True)
    shop_id = models.CharField(max_length=128,null=True)
    shop_tag = models.ManyToManyField(Shop_Tag)
    shop_address = models.CharField(max_length=240,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    shop_picture = models.ImageField(default="shop.jpg",null=True,blank=True)

    def __str__(self):
        return self.shop_name

class Product(models.Model):
    CATEGORY = (
                ('Indoor','Indoor'),
                ('Outdoor','OutDoor')
    )
    shop = models.ForeignKey(Shop,null=True,on_delete=models.SET_NULL)
    shop_owner = models.ForeignKey(Shop_Owner,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=128,null=True)
    price = models.DecimalField(null=True,max_digits=10, decimal_places=4)
    description = models.CharField(max_length=128,null=True)
    product_pic = models.ImageField(default="default_product.jpg",null=True,blank=True)
    product_tag = models.ManyToManyField(Product_Tag)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=128,choices = CATEGORY)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
                ('Pending','Pending'),
                ('Shipped','Shipped'),
                ('Delivered','Delivered')

    )
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
    note = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.status

class Customer_Post(models.Model):
    customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
    post = models.TextField(max_length=250,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    post_picutre = models.ImageField(null=True)

    def __str__(self):
        return self.post

class Shop_Owner_Post(models.Model):
    shop_owner = models.ForeignKey(Shop_Owner,null=True,on_delete=models.CASCADE)
    post = models.TextField(max_length=250,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    post_picutre = models.ImageField(null=True)

    def __str__(self):
        return self.post

class Notice(models.Model):
    notice = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.notice
