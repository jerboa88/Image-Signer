# Image Signer [Python]
![](https://img.shields.io/badge/type-Python-blue.svg "Project type")
![](https://img.shields.io/github/repo-size/jerboa88/Image-Signer.svg "Repository size")
[![](https://img.shields.io/github/license/jerboa88/Image-Signer.svg "Project license")](LICENSE.md)


A Python program to encode binary data within an image


## Installation
Python 3 and Skikit are required.


## Usage
This project is incomplete but to sign an image use `python3 imagesigner.py sign IMAGENAME "MESSAGE TO ENCODE" REPETITIONS` (ex. `python3 imagesigner.py sign image.jpg "The quick brown fox jumps over the lazy dog" 32`). Most common image file formats are accepted and `REPETITIONS` is the number of lines in the image the message is repeated. A value of -1 encodes the message on every line.

To read an image use `python3 imagesigner.py read IMAGENAME` (ex. `python3 imagesigner.py read image_signed.jpg`)

There are some other global config variables in the code. `sensitivity` is an integer that controls which color values are considered white. Higher values allow more pixels to be considered white. `verbose` toggles the printing of extra information. `opacity` controls how visible the encoded data is with respect to the original image.


## Contributing
This is a an experimental project but ideas are welcome.


## License
This project is licensed under the Mozilla Public License 2.0. See [LICENSE.md](LICENSE.md) for details.
