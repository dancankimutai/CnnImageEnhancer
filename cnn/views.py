from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .apps import CnnConfig
from .decision import enhance_image
import os
import base64
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .decision import enhance_image
from django.core.files.base import ContentFile

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from io import BytesIO
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# class Predictor:
#
#     def __init__(self, model):
#         self.model = model

def home(request):
    return render(request, 'cnn/index.html')

def enhance_image_view(request):
    global toDownload
    original_filename = None
    message = None
    if request.method == 'POST':
        if 'image' in request.FILES:
            # Handle the uploaded image

            uploaded_image = request.FILES['image']

            original_image_content = uploaded_image.read()
            original_image = SimpleUploadedFile(
                uploaded_image.name, original_image_content, content_type=uploaded_image.content_type
            )
            # Set original_filename in the session
            request.session['original_filename'] = uploaded_image.name
            # original_filename = uploaded_image.name  # Get the original filename
            enhanced_image_url, original = enhance_image(original_image)

            if enhanced_image_url is not None:
                toDownload = base64.b64decode(enhanced_image_url)

            # Render the results
            return render(
                request,
                'cnn/enhance_image.html',
                {'enhanced_image_url': enhanced_image_url, 'original_image': original, 'message': message}
            )
        else:

            # No image uploaded, display a message
            message = 'Please upload an image before starting enhancement.'

            print(message)

    return render(request, 'cnn/enhance_image.html', {'message': message})


def download_enhanced_image(request):
    if toDownload is not None:
        # Retrieve original_filename from the session
        original_filename = request.session.get('original_filename', 'default_filename.png')
        new_filename = original_filename.replace('.', '-new.')
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{new_filename}"'
        response.write(toDownload)
        return response
    else:
        return HttpResponse('No enhanced image to download')



