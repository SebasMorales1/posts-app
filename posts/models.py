from django.db import models

class Post(models.Model):
  title = models.CharField(max_length=150)
  description = models.TextField(max_length=1500, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']

class Comment(models.Model):
  text = models.CharField(max_length=450)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  published = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-published']