import os
from PIL import Image

directory = 'screenshots'
x1, y1 = 267, 207
x2, y2 = 1117, 765

for filename in os.listdir(directory):
    if filename.lower().endswith('.png'):
        image_path = os.path.join(directory, filename)
        with Image.open(image_path) as img:
            cropped_img = img.crop((x1, y1, x2, y2))
            cropped_img.save(os.path.join(directory, f"cropped_{filename}"))
            print(f"Cropped {filename} and saved as cropped_{filename}")

