import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ContentStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Content(models.Model):
    """Model representing an extensible content item in the headless CMS."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    summary = models.TextField(blank=True, default="")
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="General", db_index=True)
    status = models.CharField(
        max_length=20,
        choices=ContentStatus.choices,
        default=ContentStatus.PUBLISHED,
        db_index=True,
    )
    cover_image = models.URLField(max_length=500, blank=True, default="")
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Content"
        verbose_name_plural = "Contents"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "content"
            slug = base_slug
            counter = 1
            while Content.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if self.status == ContentStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def to_dict(self):
        """Serialize model instance to dictionary for backwards compatibility."""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "summary": self.summary,
            "author": self.author,
            "category": self.category,
            "status": self.status,
            "cover_image": self.cover_image,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat()
            if self.published_at
            else None,
        }


class MediaAsset(models.Model):
    """Media asset uploaded and managed through the headless CMS pipeline."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, default="")
    file = models.FileField(upload_to="uploads/%Y/%m/", blank=True, null=True)
    file_url = models.CharField(max_length=500, blank=True, default="")
    file_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100, default="application/octet-stream")
    file_size = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Media Asset"
        verbose_name_plural = "Media Assets"

    def __str__(self):
        return self.file_name

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "file_url": self.file_url or (self.file.url if self.file else ""),
            "file_name": self.file_name,
            "mime_type": self.mime_type,
            "file_size": self.file_size,
            "alt_text": self.alt_text,
            "created_at": self.created_at.isoformat(),
        }
