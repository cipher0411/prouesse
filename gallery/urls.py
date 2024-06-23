from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path('upload-delete-videos/', views.upload_delete_videos, name='upload_delete_videos'),
    path('display-videos/', views.display_videos, name='display_videos'),
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('video/<int:video_id>/', views.view_video, name='view_video'),
    path('image-gallery/', views.image_gallery, name='image_gallery'),
    path('upload-delete-images/', views.upload_delete_images, name='upload_delete_images'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('upload-ebook/', views.upload_ebook, name='upload_ebook'),
    path('ebooks/', views.ebook_list, name='ebook_list'),
]
