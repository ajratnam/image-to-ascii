"""A program to convert images to ASCII art."""
from collections.abc import Sequence
from typing import Optional

import numpy as np
from sty import bg, rs
from PIL import Image, ImageDraw, ImageFont, ImageGrab, ImageEnhance
from requests import get

from config import CONVERSION_CHARACTERS


def load_font(
    font_path: str, font_size: int
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(font_path, font_size)
    except OSError:
        # print(f"Load {font_path} font failed. Using default font.")
        return ImageFont.load_default()


base_font = load_font("monos.ttf", 20)


def sizeof(text: str, font: ImageFont.FreeTypeFont = base_font) -> tuple[int, int]:
    """
    Get the size of the text when rendered in the given font in pixels.

    Args:
        text: The input text to render.
        font: The font to use for the text size calculation (default: monos.ttf).

    Returns:
        size: The size of the text in pixels, (width, height).

    Examples:
        Using the default font:
        >>> sizeof("Hello World")
        (133, 20)

        Using a custom font:
        >>> custom_font = ImageFont.truetype("arial.ttf", 30)
        >>> sizeof("Hello World", custom_font)
        (155, 28)
    """
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    _, _, width, height = draw.textbbox((0, 0), text, font)
    return width, height


def ascii_to_image(text: str, font: ImageFont.FreeTypeFont = base_font) -> Image.Image:
    """
    Convert the given text to an image using the given font.

    Args:
        text: The input text to render.
        font: The font to render the text in (default: monos.ttf).

    Returns:
        text_image: The image of the rendered text.

    Examples:
        Using the default font:
        >>> ascii_to_image("Hello World")
        <PIL.Image.Image image mode=RGB size=133x20 at 0x1A9E4D77C40>

        Using a custom font:
        >>> custom_font = ImageFont.truetype("arial.ttf", 30)
        >>> ascii_to_image("Hello World", custom_font)
        <PIL.Image.Image image mode=RGB size=155x28 at 0x22E826A7C40>

        Saving the image:
        >>> image = ascii_to_image("Hello World")
        >>> image.save("hello_world.png")
    """
    text_image = Image.new("RGB", sizeof(text, font))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, (255, 255, 255), font)
    return text_image


def get_brightness_of_char(char: str, font: ImageFont.FreeTypeFont = base_font) -> int:
    """
    Get the brightness of the given character when rendered in the given font.

    Args:
        char: The character to find its brightness.
        font: The font to use to render the character (default: monos.ttf).

    Returns:
        brightness: The brightness of the character, the number of pixels that are not black.

    Examples:
        Using the default font:
        >>> get_brightness_of_char("A")
        267

        Using a custom font:
        >>> custom_font = ImageFont.truetype("arial.ttf", 30)
        >>> get_brightness_of_char("A", custom_font)
        576

        Comparing brightness of characters:
        >>> get_brightness_of_char("@") > get_brightness_of_char(".")
        True
    """
    image = ascii_to_image(char, font)
    return (np.array(image) != 0).sum().item()


sorted_letters = sorted(
    CONVERSION_CHARACTERS,
    key=lambda char: (
        get_brightness_of_char(char),
        char
    )
)


def image_to_ascii(
    image: Image.Image | str,
    size: Optional[tuple[int, int]] = None,
    charset: Optional[Sequence[str]] = None,
    fix_scaling: bool = True,
    scale: float | tuple[float, float] = 1,
    sharpness: float = 1,
    brightness: float = 1,
    sort_chars: bool = False,
    colorful: bool = False,
) -> str:
    """
    Convert image to ASCII art.

    Args:
        image: The image to convert to ASCII art, can be given as path or URL or an Image object.
            If given the string "clip" or "clipboard", it will use the image from the clipboard.
        size: The final size of the ascii art, if scale is given the scale will be applied upon this size.
        charset: Characters to use for conversion ordered in lightest to darkest, if not given will use default characters.
        fix_scaling: Whether to fix scaling of the image to preserve aspect ratio.
        scale: Scaling factor of the output image, if tuple is given it will be (width_scale, height_scale).
        sharpness: Increases the sharpness of the image by the given factor
        brightness: Increases the brightness of the image by the given factor
        sort_chars: If given an unordered charset, it will sort it by the brightness of the characters.
        colorful: Whether to use colored characters (only works on terminal).

    Returns:
        output: The ASCII art representation of the input image.

    Raises:
        ValueError: If image is invalid or cannot be loaded from path or URL.

    Examples:
        Using a custom size and charset:
        >>> print(image_to_ascii("github.png", size=(20, 20), charset="░▒▓█"))
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░▒▓▓▓████▓▓▓▒░░░░░░░░░░░░░░
        ░░░░░░░░░░░▒▓██████████████▓▒░░░░░░░░░░░
        ░░░░░░░░░▒████████████████████▒░░░░░░░░░
        ░░░░░░░░▓███▓░▒▒▓▓▓▓▓▓▓▓▒▒░▓███▓░░░░░░░░
        ░░░░░░░▓████▓░░░░░░░░░░░░░░▓████▓░░░░░░░
        ░░░░░░▒█████░░░░░░░░░░░░░░░░▓████▒░░░░░░
        ░░░░░░▓████▒░░░░░░░░░░░░░░░░▒████▓░░░░░░
        ░░░░░░▓████▓░░░░░░░░░░░░░░░░▒████▓░░░░░░
        ░░░░░░▒█████▒░░░░░░░░░░░░░░▒█████▒░░░░░░
        ░░░░░░░▓█████▓▒▒░░░░░░░░▒▒▓█████▓░░░░░░░
        ░░░░░░░░▓██▒▒████░░░░░░████████▓░░░░░░░░
        ░░░░░░░░░▒██▓▒▒▒░░░░░░░▓██████▒░░░░░░░░░
        ░░░░░░░░░░░▒▓███▓░░░░░░▓███▓▒░░░░░░░░░░░
        ░░░░░░░░░░░░░░▒▓▒░░░░░░▒▓▒░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

        Tweaking brightness and sharpness:
        >>> print(image_to_ascii("github.png", size=(20, 20), charset="░▒▓█", brightness=0.5, sharpness=0.5))
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░
        ░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░
        ░░░░░░░░▒▒▒▒▒░░░▒▒▒▒▒▒▒▒░░░▒▒▒▒▒░░░░░░░░
        ░░░░░░░▒▒▒▒▒▒░░░░░░░░░░░░░░░▒▒▒▒▒░░░░░░░
        ░░░░░░░▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒░░░░░░░
        ░░░░░░▒▒▒▒▒░░░░░░░░░░░░░░░░░░▒▒▒▒▒░░░░░░
        ░░░░░░▒▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒▒░░░░░░
        ░░░░░░░▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒░░░░░░░
        ░░░░░░░▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒░░░░░░░
        ░░░░░░░░▒▒▒▒░▒▒▒▒░░░░░░▒▒▒▒▒▒▒▒▒░░░░░░░░
        ░░░░░░░░░░▒▒▒░░░░░░░░░░▒▒▒▒▒▒▒░░░░░░░░░░
        ░░░░░░░░░░░░▒▒▒▒▒░░░░░░▒▒▒▒▒░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """
    if isinstance(image, str):
        if image.lower() in ("clip", "clipboard"):
            image = ImageGrab.grabclipboard()
            if not isinstance(image, Image.Image):
                raise ValueError("Unable to load image from clipboard")
        else:
            try:
                image = Image.open(image)
            except FileNotFoundError:
                raise ValueError("Unable to load image from path")
            except Exception:
                try:
                    image = Image.open(get(image, stream=True).raw)
                except Exception:
                    raise ValueError("Unable to load image from URL")
    if not isinstance(image, Image.Image):
        raise ValueError("Invalid image path or URL")

    image = image.convert("RGB")

    if sort_chars and charset:
        charset = sorted(
            charset,
            key=lambda char: (
                get_brightness_of_char(char),
                char
            )
        )
    charset = charset or sorted_letters

    image_width, image_height = size or image.size

    if isinstance(scale, int | float):
        scale = (scale,) * 2
    image_width = int(image_width * scale[0] * (bool(fix_scaling) + 1))
    image_height = int(image_height * scale[1])

    scaled_image = image.resize((image_width, image_height))
    brightened_image = ImageEnhance.Brightness(scaled_image).enhance(brightness)
    sharpened_image = ImageEnhance.Sharpness(brightened_image).enhance(sharpness)
    image_array = np.array(sharpened_image.convert("L"), dtype=int) * len(charset) // 256
    ascii_converted = np.vectorize(charset.__getitem__)(image_array)

    output = "\n".join(map("".join, ascii_converted))
    if colorful:
        colors = []
        for row in np.array(sharpened_image.convert("RGB")):
            for pixel in row:
                colors.append(bg(*pixel))
            colors.append(rs.bg)
        output = "".join(color + char for color, char in zip(colors, output))
    return output
