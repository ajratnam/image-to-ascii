"""A program to convert images to ASCII art."""
from collections.abc import Sequence
from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageGrab
from requests import get

from config import CONVERSION_CHARACTERS

base_font = ImageFont.truetype("monos.ttf", 20)


def sizeof(text: str, font: ImageFont.FreeTypeFont = base_font) -> tuple[int, int]:
    """
    Get the size of the text when rendered in the given font in pixels.

    Parameters
    ----------
    text: str
        The input text to render.
    font: ImageFont.FreeTypeFont, optional, default: base_font
        The font to use for the text size calculation (default: monos.ttf).

    Returns
    -------
    size: tuple[int, int]
        The size of the text in pixels, (width, height).
    """
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    _, _, width, height = draw.textbbox((0, 0), text, font)
    return width, height


def ascii_to_image(text: str, font: ImageFont.FreeTypeFont = base_font) -> Image.Image:
    """
    Convert the given text to an image using the given font.

    Parameters
    ----------
    text: str
        The input text to render.
    font: ImageFont.FreeTypeFont, optional, default: base_font
        The font to render the text in (default: monos.ttf).

    Returns
    -------
    text_image: Image.Image
        The image of the rendered text.
    """
    text_image = Image.new("RGB", sizeof(text))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, (255, 255, 255), font)
    return text_image


def get_brightness_of_char(char: str, font: ImageFont.FreeTypeFont = base_font) -> int:
    """
    Get the brightness of the given character when rendered in the given font.

    Parameters
    ----------
    char: str
        The character to find its brightness.
    font: ImageFont.FreeTypeFont, optional, default: base_font
        The font to use to render the character (default: monos.ttf).

    Returns
    -------
    brightness: int
        The brightness of the character, the number of pixels that are not black.
    """
    image = ascii_to_image(char, font)
    return (np.array(image) != 0).sum()


sorted_letters = sorted(CONVERSION_CHARACTERS, key=get_brightness_of_char)


def image_to_ascii(
    image: Image.Image | str,
    size: Optional[tuple[int, int]] = None,
    charset: Optional[Sequence[str]] = None,
    fix_scaling: bool = True,
    scale: float | tuple[float, float] = 1,
    sort_chars: bool = False,
) -> str:
    """
    Convert image to ASCII art.

    Parameters
    ----------
    image : Image.Image or str
        The image to convert to ASCII art, can be given as path or URL or an Image object.
        If given the string "clip" or "clipboard", it will use the image from the clipboard.
    size : tuple[int, int], optional
        The final size of the ascii art, if scale is given the scale will be applied upon this size.
    charset : Sequence[str], optional
        Characters to use for conversion ordered in lightest to darkest, if not given will use default characters.
    fix_scaling : bool, optional, default True
        Whether to fix scaling of the image to preserve aspect ratio.
    scale : float or tuple[float, float], optional, default 1
        Scaling factor of the output image, if tuple is given it will be (width_scale, height_scale).
    sort_chars : bool, optional, default False
        If given an unordered charset, it will sort it by the brightness of the characters.

    Returns
    -------
    output: str
        The ASCII art representation of the input image.

    Raises
    ------
    ValueError
        If image is invalid or cannot be loaded from path or URL.
    """
    if isinstance(image, str):
        if image.lower() in ("clip", "clipboard"):
            image = ImageGrab.grabclipboard()
            if not isinstance(image, Image.Image):
                raise ValueError("Unable to load image from clipboard")
        else:
            try:
                image = Image.open(image)
            except OSError:
                try:
                    image = Image.open(get(image, stream=True).raw)
                except Exception:
                    raise ValueError("Unable to load image from URL")
            except Exception:
                raise ValueError("Unable to load image from path")
    if not isinstance(image, Image.Image):
        raise ValueError("Invalid image path or URL")

    if sort_chars and charset:
        charset = sorted(charset, key=get_brightness_of_char)
    charset = charset or sorted_letters

    image_width, image_height = size or image.size

    if isinstance(scale, int | float):
        scale = (scale,) * 2
    image_width = int(image_width * scale[0] * (bool(fix_scaling) + 1))
    image_height = int(image_height * scale[1])

    scaled_image = image.resize((image_width, image_height)).convert("L")
    image_array = np.array(scaled_image, dtype=int) * len(charset) // 256
    ascii_converted = np.vectorize(charset.__getitem__)(image_array)

    output = "\n".join(map("".join, ascii_converted))
    return output
