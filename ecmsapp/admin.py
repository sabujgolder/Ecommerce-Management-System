from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Shop_Owner)
admin.site.register(Customer)
admin.site.register(Product_Tag)
admin.site.register(Shop_Tag)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer_Post)
admin.site.register(Shop_Owner_Post)
admin.site.register(Notice)
