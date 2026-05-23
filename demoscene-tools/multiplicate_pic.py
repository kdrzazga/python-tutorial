import os
from PIL import Image


def mul_pic(image_path, n):
    original = Image.open(image_path)
    width, height = original.size
    total_width = width * n
    new_image = Image.new('RGB', (total_width, height))
    for i in range(n):
        new_image.paste(original, (i * width, 0))
    return new_image


if __name__ == "__main__":
    current_path = os.getcwd()
    result = mul_pic(current_path + "\\pet.png", 5)
    result.save('bkgds.png')
    result.show()
