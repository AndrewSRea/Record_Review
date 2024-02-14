from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.models import Album, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, FloatField, Sum
from django.db.models.functions import Cast, Coalesce, Round


def login_page(request):
  page = 'login'

  page_title = 'Login'

  if request.user.is_authenticated:
    return redirect('reviews-home')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('reviews-home')
    else:
      messages.error(request, 'Username or password does not exist')

  context = {'page': page, 'page_title': page_title}
  return render(request, 'users/login_register.html', context)


def logout_user(request):
  logout(request)
  return redirect('reviews-home')


def register_page(request):
  form = UserCreationForm()
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}! Please login.')
      return redirect('login')
    else:
      form = UserCreationForm()

  context = {'form': form, 'page_title': 'Register'}
  return render(request, 'users/login_register.html', context)


def profile(request, pk):
  user = User.objects.get(id=pk)
  page_title = user.username
  albums = user.album_set.all()
  user_reviews = user.review_set.all()

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
    'user': user, 
    'albums': albums, 
    'user_reviews': user_reviews,
    'highest_rated_albums': highest_rated_albums,
    'recent_reviews': recent_reviews,
    'page_title': page_title
  }

  return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def update_profile(request):
  user = request.user
  profile = request.user.profile

  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      return redirect('profile', pk=user.id)

  else:
    u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=profile)

  context = {
    'u_form': u_form,
    'p_form': p_form,
    'page_title': 'Update Profile'
  }
  return render(request, 'users/update_profile.html', context)