from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Album(models.Model):
  creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  artist = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  image = models.ImageField(default='album_default.jpg', upload_to='album_pics')
  rating = models.IntegerField(
    choices=[(i, i) for i in range(1, 11)],
    validators=[MaxValueValidator(10), MinValueValidator(1)],
    default=10,
  )
  comment = models.TextField(null=True, blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now)

  @property
  def avg_rating(self):
    review_ratings = 0
    orig_rating = self.rating
    review_ratings_count = self.review_set.count()

    if review_ratings_count > 0:
      for review in self.review_set.all():
        review_ratings += review.rating
        ratings_sum = review_ratings + orig_rating

      ratings_count = review_ratings_count + 1
      ratings_avg = ratings_sum / ratings_count
      avg_return = round(ratings_avg, 1)

      if avg_return == 10.0:
        avg_return = 10
      else:
        avg_return = avg_return

      return avg_return

    else:
      return self.rating

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return '%s - %s' % (self.artist, self.title)


class Review(models.Model):
  reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  album = models.ForeignKey(Album, on_delete=models.CASCADE)
  rating = models.IntegerField(
    choices=[(i, i) for i in range(1, 11)],
    validators=[MaxValueValidator(10), MinValueValidator(1)],
    default=10,
  )
  comment = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now)

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return f'{self.reviewer}\'s review of {self.album.title}'