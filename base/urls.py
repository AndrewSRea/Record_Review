from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="reviews-home"),
    path('album/<str:pk>/', views.album, name="album"),
    # path('album/<str:pk>/add-review/', views.review_form, name="add-review"),

    path('create-album/', views.create_album, name="create-album"),
    path('update-album/<str:pk>/', views.update_album, name="update-album"),
    path('delete-album/<str:pk>/', views.delete_album, name="delete-album"),
    path('delete-review/<str:pk>/', views.delete_review, name="delete-review"),

    path('highest-rated-albums/', views.highest_rated, name="highest-rated"),
    path('recent-activity/', views.recent_activity, name="activity"),
]