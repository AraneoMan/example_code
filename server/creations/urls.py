from django.urls import path

from creations.views import CreationTypeListAPIView, CreationCreateAPIView, CreationFileUploadAPIView

app_name = 'creations'

urlpatterns = [
    path('types/', CreationTypeListAPIView.as_view(), name='types'),
    path('create/', CreationCreateAPIView.as_view(), name='create'),
    path('<int:creation_id>/upload-file/<str:filename>/', CreationFileUploadAPIView.as_view(), name='upload_file'),
]
