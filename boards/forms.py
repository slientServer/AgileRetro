from django import forms
from .models import Topic, Post, Category
from django.utils import timezone 
from accounts.models import User

class NewTopicForm(forms.ModelForm):
  """docstring for NewTopicForm"""
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super(NewTopicForm, self).__init__(*args, **kwargs)
    self.fields['category'] = forms.ModelChoiceField(empty_label='Please select type...', queryset=Category.objects.all().filter(entity=(User.objects.all().filter(username=user))[0].entity))

  category = forms.ModelChoiceField(queryset=Category.objects.all())

  class Meta:
    model=Topic
    fields=[ 'category', 'subject']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]

    