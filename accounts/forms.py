from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from boards.models import Entity

class SignUpForm(UserCreationForm):
  email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
  entity = forms.ModelChoiceField(empty_label = 'Please select module...', label = 'module', queryset = Entity.objects.all())

  class Meta:
    model = User
    fields = ('entity', 'username', 'email', 'password1', 'password2')

