from django.contrib import admin
from .models import User

# Register your models here.

admin.site.site_header = 'Agile Retro Administration'
admin.site.site_title = 'Agile Retro'
admin.site.register(User)
