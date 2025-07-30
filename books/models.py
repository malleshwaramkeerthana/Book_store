from django.db import models


# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=25)
    author=models.CharField(max_length=20)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    stock=models.PositiveBigIntegerField(blank=True)
    cover_image=models.URLField(blank=True)
    def __str__(self):
        return self.title
# class Order(models.Model):
#     created_at = models.DateTimeField(default=timezone.now)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()\
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.PositiveIntegerField()  # New field
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price