from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    EVENT_CHOICES = [
        ('login', 'User login'),
        ('logout', 'User logout'),
        ('verified_registered_user', 'User register'),
        ('unverified_registered_user', 'User register'),
        ('payment_success', 'User payment success'),
        ('payment_failed', 'User payment failed'),
        ('email_verification_success', 'User email verification success'),
        ('email_verification_failed', 'User email verification failed'),
        ('order_success', 'User order success'),
        ('profile_management', 'User edit profile'),
        ('delete_account', 'User account deleted'),
        ('manage_shipping', 'User updated shipping'),
        ('change_user_permissions', 'User change permissions'),
        ('update_product', 'Product update'),
        ('delete_product', 'Product deleted'),
        ('create_product', 'Product created'),
        ('create_category', 'Category created'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.user} - {self.timestamp}"
