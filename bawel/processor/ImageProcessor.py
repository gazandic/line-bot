from typing import List, Tuple

import pytesseract
import requests
import re

from os import listdir
from os.path import isfile, join
from PIL import Image
from PIL import ImageFilter

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO


class ImageProcessor:
    EMAIL_REGEX_PATTERN = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    NEWIMAGESIZE = 1200
    path = ""

    def __init__(self):
        self.image = 0

    def process_images_from_dir(self, mypath):
        self.path = mypath + '/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        return self.process_images(onlyfiles)

    # process list image to string and print it
    def process_images(self, list_url: List[str]):
        s = {}
        for url in list_url:
            s[url] = self.process_image(self.path + url) + "\n"
        return s

    # process the image to string with tesseract library
    # sharpen image first
    def process_image(self, url):
        image = self._get_image(url)
        image.filter(ImageFilter.SHARPEN)
        image = self._resize_image(image, 13)
        image.filter(ImageFilter.GaussianBlur(2))
        image.filter(ImageFilter.SMOOTH)
        image.filter(
            ImageFilter.Kernel(
                (3, 3), [
                    1, 1, 1, 0, 0, 0, -1, -1, -1]))
        print(image)
        s = pytesseract.image_to_string(image)
        return self.normalize(s)

    # get the image
    @staticmethod
    def _get_image(url):
        if "http" in url:
            return Image.open(requests.get(url), 'rb')
        return Image.open(url)

    # resize image with magnitude
    @staticmethod
    def _resize_image(image, magnitude):
        x_dim = image.size[0] * magnitude
        y_dim = image.size[1] * magnitude
        new_size = ImageProcessor.calculate_aspect_ratio(x_dim, y_dim)
        return image.resize(
            (int(
                new_size[0]), int(
                new_size[1])), Image.ANTIALIAS)

    # normalize indonesian string for small email picture
    @staticmethod
    def normalize(string: str) -> str:
        s = list(string)
        # i = 0
        # numbercount = 0
        # alphacount = 0
        # for c in s:
        #     if not self.isVowel(c):
        #         if c == 'c' and i >= 1 and s[i-1] == 'L' :
        #             s[i-1] = 'l'
        #             s.insert(i,'.')
        #         if c == 'S' :
        #             s[i] = '5'
        #         if c == '@' and s[i-1] == "." or s[i-1] == "-":
        #             del s[i-1]
        #         if c == 'g' and i >= 1 and self.isNumber(s[i-1]) and self.isNumber(s[0]):
        #             s[i] = '9'
        #         if c == 'G' and i >= 1 and self.isNumber(s[i-1]) and self.isNumber(s[0]):
        #             s[i] = '6'
        #         if c == 'Z':
        #             s[i] = '2'
        #         if c == 'O':
        #             s[i] = '0'
        #         if c == '|':
        #             s[i] = 'l'
        #     i += 1
        ss = "".join(s)
        if ImageProcessor.is_email(ss):
            is_valid = ImageProcessor.is_email(ss)
            if is_valid:
                return ss
            else:
                return ""
        else:
            return ss

    # def checkValid(self, listEmail):
    #     for key, val in listEmail.items():
    #         is_valid = validate_email(ss)
    #         if not is_valid:
    #             listEmail[key] = ""

    # check the char is vowel or not
    @staticmethod
    def is_vowel(text: str) -> bool:
        return text == 'a' or text == 'i' or text == 'u' or text == 'e' or text == 'o'

    # check the char is number and - or not
    @staticmethod
    def is_number(text: str) -> bool:
        try:
            _: float = float(text)
        except ValueError:
            return False
        finally:
            return True

    # check the char is number and - or not
    @staticmethod
    def is_email(text: str) -> bool:
        return bool(ImageProcessor.EMAIL_REGEX_PATTERN.search(text))

    # calculate aspectRatio from dimension x and y
    @staticmethod
    def calculate_aspect_ratio(x_dim: int, y_dim: int) -> Tuple[int, int]:
        # ensures images already correct size are not enlarged.
        if x_dim <= ImageProcessor.NEWIMAGESIZE and y_dim <= ImageProcessor.NEWIMAGESIZE:
            return x_dim, y_dim

        elif x_dim > y_dim:
            divider = x_dim / float(ImageProcessor.NEWIMAGESIZE)
            x_dim = float(x_dim / divider)
            y_dim = float(y_dim / divider)
            return x_dim, y_dim

        elif y_dim > x_dim:
            divider = y_dim / float(ImageProcessor.NEWIMAGESIZE)
            x_dim = float(x_dim / divider)
            y_dim = float(y_dim / divider)
            return x_dim, y_dim

        elif x_dim == y_dim:
            x_dim = ImageProcessor.NEWIMAGESIZE
            y_dim = ImageProcessor.NEWIMAGESIZE
            return x_dim, y_dim
