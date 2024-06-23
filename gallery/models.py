from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    user = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    poster_image = models.ImageField(upload_to='video_posters/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='assignments/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    



class Ebook(models.Model):
    UPLOAD_CHOICES = (
        ('url', 'URL'),
        ('pdf', 'PDF'),
    )

    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ebooks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_type = models.CharField(max_length=3, choices=UPLOAD_CHOICES)
    url = models.URLField(blank=True, null=True)
    pdf = models.FileField(upload_to='ebooks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
