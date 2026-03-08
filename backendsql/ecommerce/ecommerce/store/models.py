from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    total_amount = models.FloatField()
    payment_id = models.CharField(max_length=200,null=True,blank=True)