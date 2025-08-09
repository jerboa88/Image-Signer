<!-- Project Header -->
<div align="center"> 
  <h1 class="projectName">Image Signer</h1>

  <p class="projectBadges info">
    <img src="https://johng.io/badges/category/App.svg" alt="Project category" title="Project category">
    <img src="https://img.shields.io/github/languages/top/jerboa88/Image-Signer.svg" alt="Language" title="Language">
    <img src="https://img.shields.io/github/repo-size/jerboa88/Image-Signer.svg" alt="Repository size" title="Repository size">
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/jerboa88/Image-Signer.svg" alt="Project license" title="Project license"/>
    </a>
  </p>
  <p class="projectBadges status">
    <a href="https://unmaintained.tech/">
  		<img src="https://unmaintained.tech/badge.svg" alt="No Maintenance Intended" title="No Maintenance Intended"/>
  	</a>
   	<img src="https://img.shields.io/badge/Experimental-%E2%9A%A0%EF%B8%8E-ca8a04.svg" alt="Experimental" title="Experimental"/>
  </p>
  
  <p class="projectDesc">
    An experimental Python program to encode binary data within an image visually
  </p>
  
  <br/>
</div>


> [!IMPORTANT]
> I've marked this project as [UNMAINTAINED](https://unmaintained.tech/) because it hasn't seen an update in a while. You can still fork/download/use this project at your own risk, but I won't be able to provide support or updates.

> [!WARNING]
> This is currently an experimental project or proof-of-concept. It may contain bugs or incomplete features, and is not intended for production use. Breaking changes may be made at any time. Consider more stable alternatives for critical applications.


## About
The program works by converting the input text to binary and then modifying the brightness values of existing pixels to encode these binary values in the image. Keep in mind that the approach used for both encoding and reading data is extremely naive at the moment, and JPEG compression will likely destroy the high frequencies holding data if the image is reencoded.


## Installation
Python 3 and Skikit are required.


## Usage
### Writing to Images
**Syntax:** `python3 imagesigner.py sign IMAGENAME "MESSAGE TO ENCODE" REPETITIONS`, where `REPETITIONS` is the number of lines in the image the message is repeated. A value of -1 encodes the message on every line. Most common image file formats are accepted. Encoding images with more repetitions will result in a more accurate result as the chances of every repetition being unreadable is smaller, but will result in more visible stripes across the image.

For example, `python3 imagesigner.py sign image.jpg "The quick brown fox jumps over the lazy dog" 32` encodes the phrase `The quick brown fox jumps over the lazy dog` in binary and writes it to 32 lines in the source image, `image.jpg`.

### Reading from Images
**Syntax:** `python3 imagesigner.py read IMAGENAME`. Again, most common image file formats are accepted.

For example, `python3 imagesigner.py read image_signed.jpg` tries to extract any encoded text from the source image, `image_signed.jpg`.

### Config
There are some other global config variables in the code. `sensitivity` is an integer that controls which color values are considered white. Higher values allow more pixels to be considered white. `verbose` toggles the printing of extra information. `opacity` controls how visible the encoded data is with respect to the original image.


## Contributing
This is a an experimental project but ideas are welcome.


## License
This project is licensed under the Mozilla Public License 2.0. See [LICENSE.md](LICENSE.md) for details.


## 💕 Funding

Find this project useful? [Sponsoring me](https://johng.io/funding) will help me cover costs and **_commit_** more time to open-source.

If you can't donate but still want to contribute, don't worry. There are many other ways to help out, like:

- 📢 reporting (submitting feature requests & bug reports)
- 👨‍💻 coding (implementing features & fixing bugs)
- 📝 writing (documenting & translating)
- 💬 spreading the word
- ⭐ starring the project

I appreciate the support!
