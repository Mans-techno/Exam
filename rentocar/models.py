from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Brand(models.Model):
    title = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Car(models.Model):
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    number = models.CharField(max_length=20, unique=True)
    price_per_day = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model


class Rent(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rents')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rents')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=60)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        days = (self.end_date - self.start_date).days or 1
        self.total_price = days * self.car_id.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
