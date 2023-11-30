
import os
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from .load_model import load_and_return_model
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image as keras_image
def preprocess_image(image):
    IMAGE_SIZE = 256
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    image = image / 255.0
    return image

def enhance_image(uploaded_image):
    model = load_and_return_model()

    # Read and preprocess the in-memory image
    image_bytes = uploaded_image.read()
    input_image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    # Read and preprocess the input image
    # input_image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(input_image)

    # Model prediction
    output_image = model.predict(np.expand_dims(preprocessed_image, axis=0))
    output_image = np.squeeze(output_image, axis=0)  # Remove the batch dimension

    # Extracting components from the output
    r1 = output_image[:, :, :3]
    r2 = output_image[:, :, 3:6]
    r3 = output_image[:, :, 6:9]
    r4 = output_image[:, :, 9:12]
    r5 = output_image[:, :, 12:15]
    r6 = output_image[:, :, 15:18]
    r7 = output_image[:, :, 18:21]
    r8 = output_image[:, :, 21:24]

    x = preprocessed_image + r1 * (tf.square(preprocessed_image) - preprocessed_image)
    x = x + r2 * (tf.square(x) - x)
    x = x + r3 * (tf.square(x) - x)
    enhanced_image = x + r4 * (tf.square(x) - x)
    x = enhanced_image + r5 * (tf.square(enhanced_image) - enhanced_image)
    x = x + r6 * (tf.square(x) - x)
    x = x + r7 * (tf.square(x) - x)
    enhanced_image = x + r8 * (tf.square(x) - x)
    # # Post-processing steps
    enhanced_image = (enhanced_image.numpy() * 255).astype(np.uint8)  # Convert back to 8-bit integer

    # Convert enhanced image to base64
    enhanced_image_base64 = None
    if enhanced_image is not None:
        enhanced_image_pil = Image.fromarray(enhanced_image)
        buffered = BytesIO()
        enhanced_image_pil.save(buffered, format="PNG")
        enhanced_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    # Convert original uploaded image to base64
    original_image_base64 = None
    if uploaded_image is not None:
        uploaded_image.seek(0)  # Reset the file pointer to the beginning
        original_image_content = uploaded_image.read()
        original_image_pil = Image.open(BytesIO(original_image_content))
        buffered_original = BytesIO()
        original_image_pil.save(buffered_original, format="PNG")
        original_image_base64 = base64.b64encode(buffered_original.getvalue()).decode("utf-8")

    return enhanced_image_base64, original_image_base64



