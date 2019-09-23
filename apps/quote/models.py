from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=80)
    last_name =models.CharField(max_length=80)
    email =models.CharField(max_length=80)
    hashed_pwd = models.CharField(max_length=300)
    created_on=models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    user = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    quote = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(blank=True, default=0)
