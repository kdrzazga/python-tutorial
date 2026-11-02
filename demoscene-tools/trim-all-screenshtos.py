import os
from PIL import Image

directory = 'screenshots/p'
x1, y1 = 104, 200
x2, y2 = 728,730

for filename in os.listdir(directory):
    if filename.lower().endswith('.png'):
        image_path = os.path.join(directory, filename)
        with Image.open(image_path) as img:
            cropped_img = img.crop((x1, y1, x2, y2))
            cropped_img.save(os.path.join(directory, f"cropped_{filename}"))
            print(f"Cropped {filename} and saved as cropped_{filename}")

