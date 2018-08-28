from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class AccountsConfig(AppConfig):
    name = 'accounts'


class MyAdminConfig(AdminConfig):
    default_site = 'accounts.admin.MyAdminSite'