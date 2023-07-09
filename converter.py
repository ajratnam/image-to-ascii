import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config import CONVERSION_CHARACTERS

font = ImageFont.truetype('monos.ttf', 20)


def sizeof(text):
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    _, _, width, height = draw.textbbox((0, 0), text, font)
    return width, height


def ascii_to_image(text):
    text_image = Image.new('RGB', sizeof(text))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, (255, 255, 255), font)
    return text_image


def get_size_of_char(char):
    image = ascii_to_image(char)
    return (np.array(image) != 0).sum()


sorted_letters = sorted(CONVERSION_CHARACTERS, key=get_size_of_char)

image = Image.open('image.jpg')
image_width, image_height = image.size
scaled_image = image.resize((image_width * 2, image_height)).convert('L')

image_array = np.array(scaled_image, dtype=int) * len(sorted_letters) // 256
ascii_converted = np.vectorize(sorted_letters.__getitem__)(image_array)

output = ""
for row in ascii_converted:
    output += ''.join(row) + '\n'

ascii_to_image(output).save('text.png')
