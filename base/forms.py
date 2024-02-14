from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Album


class AlbumForm(ModelForm):
  class Meta:
    model = Album
    fields = '__all__'
    exclude = ['creator', 'created']
    labels = {
      'artist': _('Artist or Band Name'),
      'title': _('Album Title'),
      'image': _('Album Image'),
      'rating': _('Rating (1-10)'),
      'comment': _('Your Review'),
    }