import io
import re

import numpy as np
import pytest
import win32clipboard
from PIL import ImageFont, Image
from pytesseract import image_to_string

from converter import sizeof, ascii_to_image, get_brightness_of_char, image_to_ascii

url_regex = r"((http|https)://)(www.)?[a-zA-Z0-9@:%._\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)"
url_regex = re.compile(url_regex, re.IGNORECASE)


@pytest.fixture
def test_word():
    return "Hi World"


@pytest.fixture
def test_word_long():
    return "Hello World"


@pytest.fixture
def custom_font():
    return ImageFont.truetype("arial.ttf", 20)


@pytest.fixture
def custom_font_large():
    return ImageFont.truetype("arial.ttf", 30)


@pytest.fixture
def low_brightness_char():
    return "o"


@pytest.fixture
def high_brightness_char():
    return "@"


@pytest.fixture
def local_image():
    return Image.open("../images/angry_bird.jpg")


@pytest.fixture
def image_url():
    return "https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird.jpg"


@pytest.fixture
def custom_size():
    return 20, 20


@pytest.fixture
def custom_size_large():
    return 60, 60


@pytest.fixture
def custom_scale():
    return 0.5


@pytest.fixture
def custom_scale_large():
    return 2.0


def copy_to_clipboard(image):
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, output.getvalue()[14:])
        win32clipboard.CloseClipboard()


def get_size_of(image_text):
    image_ascii_string_array = image_text.splitlines()
    image_width = len(image_ascii_string_array[0])
    image_height = len(image_ascii_string_array)
    return image_width, image_height


def test_fixtures_are_valid(test_word, test_word_long, custom_font, custom_font_large, low_brightness_char, high_brightness_char, local_image, image_url):
    assert isinstance(test_word, str)
    assert isinstance(test_word_long, str)
    assert isinstance(custom_font, ImageFont.FreeTypeFont)
    assert isinstance(custom_font_large, ImageFont.FreeTypeFont)
    assert isinstance(low_brightness_char, str)
    assert isinstance(high_brightness_char, str)
    assert isinstance(local_image, Image.Image)
    assert isinstance(image_url, str)
    assert len(test_word) < len(test_word_long)
    assert custom_font.size < custom_font_large.size
    assert len(low_brightness_char) == 1
    assert len(high_brightness_char) == 1
    assert url_regex.match(image_url)


def test_sizeof_returns_size(test_word):
    size = sizeof(test_word)
    assert isinstance(size, tuple)
    assert len(size) == 2
    assert all(isinstance(x, int) for x in size)
    assert all(x >= 0 for x in size)


def test_sizeof_loads_custom_font(test_word, custom_font):
    size = sizeof(test_word, custom_font)
    assert isinstance(size, tuple)
    assert len(size) == 2
    assert all(isinstance(x, int) for x in size)
    assert all(x >= 0 for x in size)


def test_sizeof_size_increases_with_text_length(test_word, test_word_long):
    small_size = sizeof(test_word)
    large_size = sizeof(test_word_long)
    assert small_size[0] < large_size[0]
    assert small_size[1] == large_size[1]


def test_sizeof_size_increases_with_font_size(test_word, custom_font, custom_font_large):
    small_size = sizeof(test_word, custom_font)
    large_size = sizeof(test_word, custom_font_large)
    assert small_size[0] < large_size[0]
    assert small_size[1] < large_size[1]


def test_ascii_to_image_returns_image(test_word):
    image = ascii_to_image(test_word)
    assert isinstance(image, Image.Image)


def test_ascii_to_image_loads_custom_font(test_word, custom_font):
    image = ascii_to_image(test_word, custom_font)
    assert isinstance(image, Image.Image)


def test_ascii_to_image_actually_loads_font(test_word, custom_font_large):
    image = ascii_to_image(test_word, custom_font_large)
    crop_box = image.getbbox()
    assert image.size[1] == crop_box[3]


def test_ascii_to_image_writes_correct_text(test_word):
    image = ascii_to_image(test_word)
    detected_word = image_to_string(image).strip()
    assert detected_word == test_word


def test_ascii_to_image_size_increases_with_text_length(test_word, test_word_long):
    small_image = ascii_to_image(test_word)
    large_image = ascii_to_image(test_word_long)
    assert small_image.size[0] < large_image.size[0]
    assert small_image.size[1] == large_image.size[1]


def test_ascii_to_image_size_increases_with_font_size(test_word, custom_font, custom_font_large):
    small_image = ascii_to_image(test_word, custom_font)
    large_image = ascii_to_image(test_word, custom_font_large)
    assert small_image.size[0] < large_image.size[0]
    assert small_image.size[1] < large_image.size[1]


def test_get_brightness_of_char_returns_int(low_brightness_char):
    brightness = get_brightness_of_char(low_brightness_char)
    assert isinstance(brightness, int)
    assert brightness >= 0


def test_get_brightness_of_char_loads_custom_font(low_brightness_char, custom_font):
    brightness = get_brightness_of_char(low_brightness_char, custom_font)
    assert isinstance(brightness, int)
    assert brightness >= 0


def test_get_brightness_of_char_increases_with_brightness_of_char(low_brightness_char, high_brightness_char):
    low_brightness = get_brightness_of_char(low_brightness_char)
    high_brightness = get_brightness_of_char(high_brightness_char)
    assert low_brightness < high_brightness


def test_get_brightness_of_char_increases_with_font_size(low_brightness_char, custom_font, custom_font_large):
    small_brightness = get_brightness_of_char(low_brightness_char, custom_font)
    large_brightness = get_brightness_of_char(low_brightness_char, custom_font_large)
    assert small_brightness < large_brightness


def test_image_to_ascii_returns_string(local_image):
    ascii_string = image_to_ascii(local_image)
    assert isinstance(ascii_string, str)


def test_image_to_ascii_loads_from_url(image_url, local_image):
    ascii_string = image_to_ascii(image_url)
    assert isinstance(ascii_string, str)
    assert ascii_string == image_to_ascii(local_image)


def test_image_to_ascii_loads_from_clipboard(local_image):
    copy_to_clipboard(local_image)
    ascii_string = image_to_ascii("clip")
    assert isinstance(ascii_string, str)
    assert ascii_string == image_to_ascii(local_image)


def test_image_to_ascii_creates_correct_size(local_image):
    ascii_string = image_to_ascii(local_image)
    ascii_string_array = np.array(list(ascii_string))
    width, height = local_image.size
    assert np.where(ascii_string_array == "\n")[0].tolist() == list(range(2 * width, 2 * width * height, 2 * width + 1))


def test_image_to_ascii_creates_correct_size_when_scaling_is_not_fixed(local_image):
    ascii_string = image_to_ascii(local_image, fix_scaling=False)
    ascii_string_array = np.array(list(ascii_string))
    width, height = local_image.size
    assert np.where(ascii_string_array == "\n")[0].tolist() == list(range(width, width * height, width + 1))


def test_image_to_ascii_resizes_to_custom_size(local_image, custom_size):
    ascii_string = image_to_ascii(local_image, size=custom_size, fix_scaling=False)
    ascii_string_array = np.array(list(ascii_string))
    width, height = custom_size
    assert np.where(ascii_string_array == "\n")[0].tolist() == list(range(width, width * height, width + 1))


def test_image_to_ascii_increases_with_custom_image_size(local_image, custom_size, custom_size_large):
    small_ascii_string = image_to_ascii(local_image, size=custom_size, fix_scaling=False)
    large_ascii_string = image_to_ascii(local_image, size=custom_size_large, fix_scaling=False)
    assert len(small_ascii_string) < len(large_ascii_string)


def test_image_to_ascii_scales(local_image, custom_scale):
    original_ascii_string = image_to_ascii(local_image, fix_scaling=False)
    scaled_ascii_string = image_to_ascii(local_image, scale=custom_scale, fix_scaling=False)
    original_width, original_height = get_size_of(original_ascii_string)
    scaled_width, scaled_height = get_size_of(scaled_ascii_string)
    assert scaled_width == int(original_width * custom_scale)
    assert scaled_height == int(original_height * custom_scale)


def test_image_to_ascii_increases_with_scaling_factor(local_image, custom_scale, custom_scale_large):
    small_ascii_string = image_to_ascii(local_image, scale=custom_scale, fix_scaling=False)
    large_ascii_string = image_to_ascii(local_image, scale=custom_scale_large, fix_scaling=False)
    original_width, original_height = get_size_of(small_ascii_string)
    scaled_width, scaled_height = get_size_of(large_ascii_string)
    assert scaled_width == int(original_width * custom_scale_large / custom_scale)
    assert scaled_height == int(original_height * custom_scale_large / custom_scale)


def test_image_to_ascii_conjunction_of_scale_and_custom_size(local_image, custom_scale, custom_size):
    ascii_string = image_to_ascii(local_image, scale=custom_scale, size=custom_size, fix_scaling=False)
    width, height = get_size_of(ascii_string)
    assert width == int(custom_size[0] * custom_scale)
    assert height == int(custom_size[1] * custom_scale)
