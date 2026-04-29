from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """One-To-One relationship مع User الافتراضي"""

    class Role(models.TextChoices):
        OWNER = 'owner', 'مالك مساحة'
        TENANT = 'tenant', 'مستأجر'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.TENANT)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def is_owner(self):
        return self.role == self.Role.OWNER

    def is_tenant(self):
        return self.role == self.Role.TENANT
