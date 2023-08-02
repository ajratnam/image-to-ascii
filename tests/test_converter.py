import pytest
from PIL import ImageFont, Image

from converter import sizeof, ascii_to_image


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
