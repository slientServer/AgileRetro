from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

# Create your models here.

class  Board(models.Model):
  """docstring for  Board"""
  name=models.CharField(max_length=30, unique=True)
  description=models.CharField(max_length=1000)
  def __str__(self):
    return self.name

  def get_posts_count(self):
      return Post.objects.filter(topic__board=self).count()

  def get_last_post(self):
      return Post.objects.filter(topic__board=self).order_by('-created_at').first()
  

class Topic(models.Model):
  subject = models.TextField(max_length=1000)
  last_updated = models.DateTimeField(auto_now_add=True)
  board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name='topics')
  starter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='topics')
  views = models.PositiveIntegerField(default=0)
  def __str__(self):
    return self.name

class Post(models.Model):
  """docstring for Post"""
  message=models.TextField(max_length=4000)
  topic=models.ForeignKey(Topic, related_name="posts", on_delete=models.PROTECT)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(null=True)
  created_by=models.ForeignKey(User, related_name="posts", on_delete=models.PROTECT)
  updated_by=models.ForeignKey(User, null=True, related_name="+", on_delete=models.PROTECT)
  post_type=models.CharField(max_length=1000, default="post")
  def __str__(self):
    truncated_message = Truncator(self.message)
    return truncated_message.chars(30)
  def get_message_as_markdown(self):
    return mark_safe(markdown(self.message, safe_mode='escape'))

    



