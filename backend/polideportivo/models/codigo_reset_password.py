from django.db import models
from django.utils import timezone
from datetime import timedelta

class CodigoResetPassword(models.Model):
    email = models.EmailField()
    codigo = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def isValid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)