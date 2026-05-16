from django.db import models
from django.conf import settings
from django.utils.text import slugify


class LearningCategory(models.Model):
    """Modules like Foundations, Stocks, T-Bills, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome class
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Learning Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Video(models.Model):
    """Main Video Content"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    category = models.ForeignKey(LearningCategory, on_delete=models.CASCADE, related_name='videos')
    
    description = models.TextField()
    video_url = models.FileField(upload_to='videos/', null=True, blank=True)  # Local video
    youtube_url = models.URLField(blank=True)  # Alternative: YouTube embed
    
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    
    duration = models.CharField(max_length=20, help_text="e.g., 12:45")  # Minutes
    
    module_number = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)
    
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'module_number']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module_number}. {self.title}"


class UserVideoProgress(models.Model):
    """Track user progress"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    
    watched = models.BooleanField(default=False)
    watch_time = models.PositiveIntegerField(default=0, help_text="Seconds watched")
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.email} - {self.video.title}"
    