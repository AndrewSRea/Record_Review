from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile


class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['image', 'bio']
    labels = {
      'image': _('Profile Photo'),
    }