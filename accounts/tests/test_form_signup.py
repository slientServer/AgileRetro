from django.test import TestCase
from ..forms import SignUpForm

class  SignUpFormTest(TestCase):
  """docstring for  SignUpFormTest"""
  def test_form_has_fields(self):
    form = SignUpForm()
    expected = ['username', 'email', 'password1', 'password2',]
    actual = list(form.fields)
    self.assertSequenceEqual(expected, actual)