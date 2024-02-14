from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, FloatField, Q, Sum, When
from django.db.models.functions import Cast, Coalesce, Round
from django.core.paginator import Paginator, EmptyPage
from .models import Album, Review
from .forms import AlbumForm


def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''

  albums = Album.objects.filter(Q(artist__icontains=q) | Q(title__icontains=q))

  paginator = Paginator(albums, 5)

  page_number = request.GET.get('page', 1)

  try:
    page = paginator.page(page_number)
  except EmptyPage:
    page = paginator.page(1)


  album_count = albums.count()

  highest_rated_albums = Album.objects.annotate(
    combined_ratings=Round(
      Cast(
        (Coalesce(Sum('rating', distinct=True), 0) + Coalesce(Sum('review__rating'), 0)),
        output_field=FloatField()
      ) / (Coalesce(Count('review__rating'), 0) + 1),
      precision=2
    )
  ).order_by('-combined_ratings')[0:5]

  recent_reviews = Review.objects.all()[0:5]

  context = {
    'albums': page, 
    'album_count': album_count,
    'highest_rated_albums': highest_rated_albums,
    'recent_reviews': recent_reviews
  }
  return render(request, 'base/home.html', context)


def album(request, pk):
  album = Album.objects.get(id=pk)
  page_title = Album.objects.get(id=pk).title
  reviews = album.review_set.all().order_by('-created')

  if request.method == 'POST':
    review = Review.objects.create(
      reviewer=request.user,
      album=album,
      rating=request.POST.get('rating'),
      comment=request.POST.get('comment')
    )
    return redirect('album', pk=album.id)

  highest_rated_albums = Album.objects.annotate(
    combined_ratings=Round(
      Cast(
        (Coalesce(Sum('rating', distinct=True), 0) + Coalesce(Sum('review__rating'), 0)),
        output_field=FloatField()
      ) / (Coalesce(Count('review__rating'), 0) + 1),
      precision=2
    )
  ).order_by('-combined_ratings')[0:5]

  recent_reviews = Review.objects.all()[0:5]

  context = {
    'album': album, 
    'page_title': page_title, 
    'reviews': reviews,
    'highest_rated_albums': highest_rated_albums,
    'recent_reviews': recent_reviews
  }
  return render(request, 'base/album.html', context)


# REVIEW FORM (Look in the documentation to see if there is a way to restrict a user from submitting a
# ReviewForm if they're not logged in.)
# def review_form(request, pk):
#   album = Album.objects.get(id=pk)
#   if request.method == 'POST':
#     form = ReviewForm(request.POST)
#     if form.is_valid():
#       review = form.save(commit=False)
#       review.reviewer = request.user
#       review.album = album
#       review.save()
#       return redirect('album', pk=album.id)
#   else:
#     form = ReviewForm()

#   return render(request, 'base/review_form.html', {'form': form, 'album': album})


@login_required(login_url='login')
def create_album(request):
  form = AlbumForm()
  if request.method == 'POST':
    form = AlbumForm(request.POST, request.FILES)
    if form.is_valid():
      album = form.save(commit=False)
      album.creator = request.user
      form.save()
      return redirect('reviews-home')

  context = {'form': form, 'page_title': 'Create Album'}
  return render(request, 'base/album_form.html', context)


@login_required(login_url='login')
def update_album(request, pk):
  album = Album.objects.get(id=pk)
  form = AlbumForm(instance=album)

  if request.user != album.creator:
    messages.error(request, 'You do not have permission to edit this album.')

  if request.method == 'POST':
    form = AlbumForm(request.POST, request.FILES, instance=album)
    if form.is_valid():
      form.save()
      return redirect('reviews-home')

  page_title = Album.objects.get(id=pk).title

  context = {'form': form, 'page_title': f'Update {page_title}'}
  return render(request, 'base/album_form.html', context)
  

@login_required(login_url='login')
def delete_album(request, pk):
  album = Album.objects.get(id=pk)
  if request.method == 'POST':
    album.delete()
    return redirect('reviews-home')

  page_title = Album.objects.get(id=pk).title

  context = {'obj': album, 'page_title': f'Delete {page_title}'}
  return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_review(request, pk):
  review = Review.objects.get(id=pk)

  if request.user != review.reviewer:
    messages.error(request, 'Only the creator of this review may delete this review.')

  if request.method == 'POST':
    review.delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('album', pk=review.album.id)

  context = {'obj': review, 'page_title': 'Delete Review'}
  return render(request, 'base/delete.html', context)


def highest_rated(request):
  albums = Album.objects.all()
  reviews = Review.objects.all()

  highest_rated_albums = Album.objects.annotate(
    combined_ratings=Round(
      Cast(
        (Coalesce(Sum('rating', distinct=True), 0) + Coalesce(Sum('review__rating'), 0)),
        output_field=FloatField()
      ) / (Coalesce(Count('review__rating'), 0) + 1),
      precision=2
    )
  ).order_by('-combined_ratings')[0:10]  

  context = {
    'albums': albums, 
    'reviews': reviews, 
    'highest_rated_albums': highest_rated_albums,
    'page_title': 'Highest Rated Albums'
  }

  return render(request, 'base/highest_rated.html', context)


def recent_activity(request):
  album_reviews = Review.objects.all()[0:10]

  context = {'album_reviews': album_reviews, 'page_title': 'Recent Activity'}
  return render(request, 'base/activity.html', context)