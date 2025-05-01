from django.db import models
from django.contrib.auth.models import User

# Extend the built-in User model with additional fields if needed
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=42, blank=True, null=True)  # For Web3 wallet address

    def __str__(self):
        return self.user.username