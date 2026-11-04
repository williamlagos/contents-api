from django.db import models
from django.utils import timezone


class Content(models.Model):
    """Model representing a content item in the headless CMS."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Content"
        verbose_name_plural = "Contents"

    def __str__(self):
        return self.title

    def to_dict(self):
        """Serialize model instance to dictionary for backwards compatibility."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
