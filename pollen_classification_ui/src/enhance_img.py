import os
import cv2
from PIL import Image, ImageEnhance

def enhance_image(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Upscale the image to 100x100
    img = img.resize((100, 100))

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.25)  # Increase contrast by 50%

    # Increase brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.25)  # Increase brightness by 50%

    # Save the enhanced image
    img.save(image_path)

def search_and_enhance(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                enhance_image(image_path)

# Replace with your directory
directory = r"//wsl.localhost/Ubuntu/home/mcagriaksoy/pollen_multi_class_ai/pollen_classification_ui/referans_polen"
search_and_enhance(directory)