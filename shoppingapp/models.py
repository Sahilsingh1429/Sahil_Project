from django.db import models
from sellerapp.models import *
# Create your models here.

class User(models.Model):
    v1 = [('Male','Male'),
          ('Female','Female'),
          ('Others','Others')]
    
    
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=50,choices=v1)
    pic = models.FileField(upload_to='profile_pics',default='happy.jpg')
    
    
    
    def __str__(self):
        return self.first_name
    
    
class Cart(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)