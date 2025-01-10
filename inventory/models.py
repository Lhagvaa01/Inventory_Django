from django.db import models
import random
import string
from django.utils.timezone import now

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Компанийн нэр
    register = models.CharField(max_length=10, unique=True)  # Регистерийн дугаар
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.register})"

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    special_code = models.CharField(max_length=5, unique=True, editable=False)
    app_usage_period = models.DateTimeField(null=True, blank=True)
    imei_code = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.special_code:
            self.special_code = self.generate_special_code()
        super().save(*args, **kwargs)

    def generate_special_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def __str__(self):
        return f"{self.username} ({self.company.name})"

    def is_app_active(self):
        return self.app_usage_period and self.app_usage_period > now()


class Inventory(models.Model):
    barcode = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barcode} - {self.quantity}"
