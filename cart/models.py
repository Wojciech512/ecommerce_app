from django.contrib.auth.models import User
from django.db import models

class SavedCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="saved_cart")
    cart_data = models.JSONField(default=dict)

    def __str__(self):
        return f"User cart: {self.user.username}"
