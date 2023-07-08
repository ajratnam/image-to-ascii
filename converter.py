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
