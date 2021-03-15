from django.contrib import admin
from .models import (
  Customer,
  Product,
  Card,
  OrderPlaced
  )
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display =['id','user','name','localty','city','zipcode','state']
  
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display=['title','selling_price','discounted_price','description','brand','category','product_image']
  
@admin.register(Card)
class CardModelAdmin(admin.ModelAdmin):
  list_display=['user','product','quantity']
  
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
  list_display=['user','customer','product','quantity','order_date','status']