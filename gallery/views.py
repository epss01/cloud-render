from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count
import cloudinary.uploader

from .models import Album, Photo
from .forms import AlbumForm, PhotoForm, CustomUserCreationForm
from .mixins import OwnerOrAdminMixin


# ──────────────────────────────────────────────
# Album Views
# ──────────────────────────────────────────────

class AlbumListView(ListView):
    """Home page: displays all albums with search & pagination."""
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'
    paginate_by = 9

    def get_queryset(self):
        queryset = Album.objects.annotate(
            num_photos=Count('photos')
        ).select_related('created_by')

        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class AlbumDetailView(DetailView):
    """Displays a single album with its photos."""
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = self.object.photos.select_related('uploaded_by')

        query = self.request.GET.get('q', '')
        if query:
            photos = photos.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        context['photos'] = photos
        context['query'] = query
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    """Create a new album. Requires login."""
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Album created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album_detail', kwargs={'pk': self.object.pk})


class AlbumUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    """Edit an album. Only the owner or admin can access."""
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    owner_field = 'created_by'

    def form_valid(self, form):
        messages.success(self.request, 'Album updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album_detail', kwargs={'pk': self.object.pk})


class AlbumDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    """Delete an album. Only the owner or admin can access."""
    model = Album
    template_name = 'gallery/album_confirm_delete.html'
    success_url = reverse_lazy('album_list')
    owner_field = 'created_by'

    def form_valid(self, form):
        album = self.get_object()
        # Delete all associated Cloudinary images
        for photo in album.photos.all():
            if photo.image:
                try:
                    cloudinary.uploader.destroy(photo.image.public_id)
                except Exception:
                    pass
        # Delete album cover from Cloudinary
        if album.cover_image:
            try:
                cloudinary.uploader.destroy(album.cover_image.public_id)
            except Exception:
                pass
        messages.success(self.request, f'Album "{album.title}" deleted.')
        return super().form_valid(form)


# ──────────────────────────────────────────────
# Photo Views
# ──────────────────────────────────────────────

class PhotoCreateView(LoginRequiredMixin, CreateView):
    """Add a photo to an album. Requires login."""
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, pk=self.kwargs['album_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Photo uploaded successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.album
        return context

    def get_success_url(self):
        return reverse('album_detail', kwargs={'pk': self.album.pk})


class PhotoUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    """Edit a photo. Only the uploader or admin can access."""
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'
    owner_field = 'uploaded_by'

    def form_valid(self, form):
        messages.success(self.request, 'Photo updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.object.album
        return context

    def get_success_url(self):
        return reverse('album_detail', kwargs={'pk': self.object.album.pk})


class PhotoDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    """Delete a photo. Only the uploader or admin can access."""
    model = Photo
    template_name = 'gallery/photo_confirm_delete.html'
    owner_field = 'uploaded_by'

    def form_valid(self, form):
        photo = self.get_object()
        album_pk = photo.album.pk
        # Remove image from Cloudinary
        if photo.image:
            try:
                cloudinary.uploader.destroy(photo.image.public_id)
            except Exception:
                pass
        messages.success(self.request, f'Photo "{photo.title}" deleted.')
        self.success_url = reverse('album_detail', kwargs={'pk': album_pk})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album_detail', kwargs={'pk': self.object.album.pk})


# ──────────────────────────────────────────────
# Authentication Views
# ──────────────────────────────────────────────

class RegisterView(CreateView):
    """User registration with auto-login on success."""
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Welcome, {self.object.username}! Your account has been created.')
        return response