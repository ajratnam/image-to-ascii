# image-to-ascii
A python program to convert an image into an ascii image

## Introduction

This program allows you to convert images into ASCII art. It uses various parameters to control the conversion process, including image scaling, sharpness adjustment, brightness adjustment, character set, and more.

## Installation

1. Clone this repository to your local machine.
    ```bash
    git clone https://www.github.com/ajratnam/image-to-ascii.git
    ```
2. Activate the poetry environment.
    ```bash
    poetry shell
    ```
3. Install the dependencies.
    ```bash
    poetry install
    ```

## Usage

The documentation for the program can be read [here](https://ajratnam.github.io/image-to-ascii/).


## Examples

Here are some examples of how to use the program:

### Convert an image to ASCII art.
```py
from converter import image_to_ascii
print(image_to_ascii('images/angry_bird.jpg'))
```
This converts the image to ASCII art and prints it to the console.
![ascii_angry_bird](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii.jpg)


### Save the ASCII art to an image.
```py
from converter import image_to_ascii, ascii_to_image
ascii_art = image_to_ascii('images/angry_bird.jpg')
ascii_art_image = ascii_to_image(ascii_art)
ascii_art_image.save('images/angry_bird_ascii.jpg')
```
This saves the ASCII art to an image file on your computer.


### Change the size of the ascii art by absolute pixels.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", size=(30, 30)))
```
This resizes the ASCII art to look like 30x30 characters(but it is actually 60x30 pixels).
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_resized.jpg)


### Change the size of the ascii art by absolute pixels but do not try to maintain visual aspect ratio.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", size=(30, 30), fix_scaling=False))
```
This resizes the ASCII art to 30x30 characters.

![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_resized_actual_size.jpg)


### Change the size of the ascii art by relative scaling.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", scale=0.5))
```
This resizes the ASCII art to 50% of the original size.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_scaled.jpg)


### Brighten the ascii art.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", brightness=3))
```
This increases the brightness of the ASCII art to 3 times the original.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_brightened.jpg)


### Darken the ascii art.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", brightness=0.2))
```
This decreases the brightness of the ASCII art to 20% of the original.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_darkened.jpg)


### Sharpen the ascii art.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", sharpness=3))
```
This increases the sharpness of the ASCII art to 3 times the original.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_sharpened.jpg)


### Blur the ascii art.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", sharpness=0.2))
```
This decreases the sharpness of the ASCII art to 20% of the original.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_blurred.jpg)


### Change the character set used to generate the ascii art.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", charset=' ░▒▓█'))
```
Changes the characters used to generate the ASCII art.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_custom_charset.jpg)


### Print colored ascii art to the console.
```py
from converter import image_to_ascii
print(image_to_ascii("images/angry_bird.jpg", colorful=True))
```
Prints the ASCII art colorfully to the console.
![ascii_angry_bird_resized](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/images/angry_bird_ascii_colored.jpg)


## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/ajratnam/image-to-ascii/main/LICENSE).

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to create an issue or a pull request.
Install the additional development dependencies with `poetry install --dev`.
Run coverage test with `python -m pytest --cov`