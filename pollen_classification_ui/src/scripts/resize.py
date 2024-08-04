import os
from PIL import Image

def resize_images_in_folder(folder, width, height):
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            try:
                img = Image.open(path)
                img = img.resize((width, height), Image.BICUBIC)
                img.save(path)
            except Exception as e:
                print(f"Unable to resize image {path}. Error: {str(e)}")
        elif os.path.isdir(path):
            resize_images_in_folder(path, width, height)

# Usage
resize_images_in_folder('path_to_your_folder', 128, 128)