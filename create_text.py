# import required classes
import os
from PIL import Image, ImageDraw, ImageFont
import re
import numpy as np
import sys

from general_tools import utils

## Input file path
#input_text_path = r"./text/tiny_shakespeare.txt"
input_text_path = r"./text/input.txt"
font_folder = r"./fonts/font_pack"

def open_file(path):
    with open(path, "r") as f:
        return "".join(f.readlines())

class TextGenerator():

    def __init__(self, font_name="FAREWELL.TTF"):
        input_text = open_file(input_text_path)
        self.cleaned_text = self.clean_message(input_text)
        self.tracker = 0

        # FONT
        self.font_path = os.path.join(font_folder, font_name)

        ## Output
        self.output_path = os.path.join(r"./data/", font_name[:-4])
        utils.make_dir(self.output_path)


    def get_next_picture(self, save=True):
        if self.tracker + 50 > len(self.cleaned_text):
            self.tracker = 0

        rd = np.random.randint(35, 40)
        rd += self.cleaned_text[self.tracker + rd:].find(" ")  # end on a space
        self.create_image(self.font_path, self.cleaned_text[self.tracker:self.tracker + rd],save=save)
        self.tracker += rd

    def clean_message(self,message):
        return re.sub('[^a-zA-Z,.?!;: ]', ' ', message)


    def create_image(self,font_path, message, output_name=None,save=True):
        if output_name is None:
            output_name = message + ".png"
        if output_name[-4:] != ".png":
            output_name += ".png"

        # create Image object with the input image

        #image = Image.open('background.png')
        image = Image.new('RGBA', (600, 100), (255, 255, 255, 255))

        # initialise the drawing context with
        # the image object as background

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, size=84)

        # starting position of the message

        (x, y) = (10, 50)
        color = 'rgb(0, 0, 0)'  # black color

        # draw the message on the background
        draw.text((x, y), message, fill=color, font=font)

        # save the edited image
        if save:
            image.save(os.path.join(self.output_path, output_name))
        else:
            return image


if __name__ == '__main__':
    tg=TextGenerator()
    while True:
        tg.get_next_picture(save=False)