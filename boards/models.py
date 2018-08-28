# -*- coding: utf-8 -*-

from django.db import models
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Entity(models.Model):
  """docstring for Company"""
  name = models.CharField(max_length = 30, unique = True)
  description = models.CharField(max_length = 1000)
  status = models.CharField(max_length=8, choices= (('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('deleted', 'Deleted'),), default = 'active')

  def __str__(self):
    return self.name

class Category(models.Model):
  """docstring for Company"""
  name = models.CharField(max_length = 30, unique = True)
  description = models.CharField(max_length = 1000)
  entity = models.ForeignKey(Entity, on_delete = models.PROTECT, related_name = 'categorys')

  def __str__(self):
    return self.name

class  Board(models.Model):
  """docstring for  Board"""
  name = models.CharField(max_length = 30)
  description = models.CharField(max_length = 1000)
  entity = models.ForeignKey(Entity, on_delete = models.PROTECT, related_name = 'boards')
  status = models.CharField(max_length=8, choices= (('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('deleted', 'Deleted'),), default = 'active')
  start = models.DateTimeField( default=timezone.now )
  end = models.DateTimeField( default=timezone.now )

  def __str__(self):
    return self.name

  def get_posts_count(self):
      return Post.objects.filter(topic__board = self).count()

  def get_last_post(self):
      return Post.objects.filter(topic__board = self).order_by('-created_at').first()
  
class Topic(models.Model):
  subject = models.TextField(max_length = 1000)
  last_updated = models.DateTimeField(auto_now_add = True)
  board = models.ForeignKey(Board, on_delete = models.PROTECT, related_name = 'topics')
  category = models.ForeignKey(Category, on_delete = models.PROTECT, related_name = 'topics', null = True)
  starter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'topics')
  views = models.PositiveIntegerField(default = 0)
  status = models.CharField(max_length=8, choices= (('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('deleted', 'Deleted'),), default = 'active')

  def __str__(self):
    return self.subject

class Post(models.Model):
  """docstring for Post"""
  message = models.TextField(max_length = 4000)
  topic = models.ForeignKey(Topic, related_name = "posts", on_delete = models.PROTECT)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(null = True)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "posts", on_delete = models.PROTECT)
  updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, related_name = "+", on_delete = models.PROTECT)
  post_type = models.CharField(max_length = 1000, default = "post")
  status = models.CharField(max_length=8, choices= (('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('deleted', 'Deleted'),), default = 'active')


  def __str__(self):
    truncated_message = Truncator(self.message)
    return truncated_message.chars(30)
  def get_message_as_markdown(self):
    return mark_safe(markdown(self.message, safe_mode = 'escape'))

    



