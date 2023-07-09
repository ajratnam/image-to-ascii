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


def image_to_ascii(image, size=None, charset=None, fix_scaling=True, sort_chars=False):
    if sort_chars and charset:
        charset = sorted(charset, key=get_size_of_char)
    charset = charset or sorted_letters
    image_width, image_height = size or image.size
    image_width *= bool(fix_scaling) + 1
    scaled_image = image.resize((image_width, image_height)).convert('L')

    image_array = np.array(scaled_image, dtype=int) * len(charset) // 256
    ascii_converted = np.vectorize(charset.__getitem__)(image_array)

    output = '\n'.join(map(''.join, ascii_converted))
    ascii_to_image(output).save('text5.png')
    return output


image = Image.open('image.jpg')
with open('converted.txt', 'w+') as file:
    file.write(image_to_ascii(image))
