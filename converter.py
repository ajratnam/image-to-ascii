import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config import CONVERSION_CHARACTERS

font = ImageFont.truetype('arial.ttf', 20)


def get_size_of_char(char):
    image = Image.new('RGB', (30, 30))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), char, font=font, fill=(255, 255, 255))
    return (np.array(image) != 0).sum()


sorted_letters = sorted(CONVERSION_CHARACTERS, key=get_size_of_char)

image = Image.open('image.jpg')
width, height = image.size
scaled_image = image.resize((width * 2, height)).convert('L')

image_array = np.array(scaled_image, dtype=int) * len(sorted_letters) // 256
ascii_converted = np.vectorize(sorted_letters.__getitem__)(image_array)

with open('ascii.txt', 'w') as f:
    for row in ascii_converted:
        f.write(''.join(row) + '\n')
