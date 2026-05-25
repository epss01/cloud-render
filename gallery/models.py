from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Album(models.Model):
    """Represents a photo album owned by a user."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField('cover', blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='albums'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    """Represents a photo within an album, stored on Cloudinary."""
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='photos'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField('image')
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='photos'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title