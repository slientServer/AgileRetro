from django.contrib import admin
from .models import Entity, Board, Topic, Post, Category
# Register your models here.

admin.site.register(Entity)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Category)