from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

class Story(models.Model):

    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivial News'),
    ]
    REGION_CHOICES = [
        ('uk', 'United Kingdom'),
        ('eu', 'European Union'),
        ('w', 'World News'),
    ]

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)   
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=128)

# Create your models here.
