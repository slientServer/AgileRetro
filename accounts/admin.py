from django.contrib import admin
from .models import User

# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = 'Agile-Retro Administration'

admin.register(User)
