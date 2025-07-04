from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
import uuid


# Create your models here.

User = get_user_model()


class FitnessBlog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/images/%Y/%m/%d/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=[("DF", "Draft"), ("PB", "Published")], default="DF")

    def __str__(self):
        return f"{self.title}"




class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    start_time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return f"Booking {self.id} for {self.user}"
