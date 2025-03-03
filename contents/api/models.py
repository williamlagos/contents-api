from django.db import models
from django.utils import timezone


class Content(models.Model):
    """Model representing a content item."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
