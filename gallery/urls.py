from django.urls import path
from . import views

urlpatterns = [
    # Album URLs
    path('', views.AlbumListView.as_view(), name='album_list'),
    path('album/create/', views.AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album_edit'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),

    # Photo URLs
    path('album/<int:album_pk>/photo/add/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo_edit'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),

    # Auth URLs
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
]
