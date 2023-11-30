from django.urls import path
from . import views

urlpatterns = [
    path('enhance/', views.enhance_image_view, name='enhance_image'),
    path('', views.home, name=''),
    path('download_enhanced_image/', views.download_enhanced_image, name='download_enhanced_image'),

    # Add other URL patterns if needed
]
