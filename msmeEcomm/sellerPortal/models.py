from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import logging

logger = logging.getLogger(__name__)

class SellerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        logger.info(f"Seller {user.email} created successfully.")
        return user

class Seller(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    niche = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'specialization', 'niche']

    objects = SellerManager()

    def __str__(self):
        return self.email
    
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            logger.info(f"Creating new product: {self.name} for seller {self.seller.email}")
        else:
            logger.info(f"Updating product: {self.name} for seller {self.seller.email}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Deleting product: {self.name} for seller {self.seller.email}")
        super().delete(*args, **kwargs)