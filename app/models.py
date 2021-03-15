from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

STATE_CHOISES=(
  ('Egypt giza Cairo ','giza'),
  ('Saudia ','Saudia'),
  ('Redmi','Redmi'),
  ('Samsung','Samsung')
  )
  
class Customer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
  name = models.CharField(max_length=200)
  localty = models.CharField(max_length=200)
  city = models.CharField(max_length=50)
  zipcode = models.IntegerField()
  state = models.CharField(choices=STATE_CHOISES,max_length=40)
  
  def __str__(self):
    return str(self.id)
    
    
  
CATEGORY_CHOISES=(
  ('M','Mobile'),
  ('L','Laptop'),
  ('TW','Top Wear'),
  ('BW','Bottom Wear'),
  )


class Product(models.Model):
  title = models.CharField(max_length=100)
  selling_price= models.FloatField()
  discounted_price = models.FloatField()
  description = models.TextField()
  brand = models.CharField(max_length=100)
  category =models.CharField(choices=CATEGORY_CHOISES,max_length=2)
  product_image=models.ImageField(upload_to='productimg')
  
  def __str__(self):
    return str(self.id)
    
    
class Card(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  
  def __str__(self):
    return str(self.id)
    
  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price
    
    
STATUS_CHOISES=(
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cansel','Cansel'),
  )
  
  
class OrderPlaced(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  order_date=models.DateTimeField(auto_now_add=True)
  status =models.CharField(choices=STATUS_CHOISES,max_length=50,default='panding')
  
  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price