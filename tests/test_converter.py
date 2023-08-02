import pytest
from PIL import ImageFont, Image
from pytesseract import image_to_string

from converter import sizeof, ascii_to_image, get_brightness_of_char


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


def test_fixtures_are_valid(test_word, test_word_long, custom_font, custom_font_large, low_brightness_char, high_brightness_char):
    assert isinstance(test_word, str)
    assert isinstance(test_word_long, str)
    assert isinstance(custom_font, ImageFont.FreeTypeFont)
    assert isinstance(custom_font_large, ImageFont.FreeTypeFont)
    assert isinstance(low_brightness_char, str)
    assert isinstance(high_brightness_char, str)
    assert len(test_word) < len(test_word_long)
    assert custom_font.size < custom_font_large.size
    assert len(low_brightness_char) == 1
    assert len(high_brightness_char) == 1


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
