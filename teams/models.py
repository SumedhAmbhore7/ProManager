from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_orgs')

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('member', 'Member')
    ], default='member')

    def __str__(self):
        return f"{self.user.username} in {self.organization.name}"
