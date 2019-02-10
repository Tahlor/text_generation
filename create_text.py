# import required classes
import os
from PIL import Image, ImageDraw, ImageFont # pip install pillow
import re
import numpy as np
import sys

from general_tools import utils


def open_file(path):
    with open(path, "r") as f:
        return "".join(f.readlines())

class TextGenerator():

    def __init__(self, input_text_path = r"./text/tiny_shakespeare.txt", font_folder=r"./fonts/font_pack", output_path="./data"):
        input_text = open_file(input_text_path)
        self.cleaned_text = self.clean_message(input_text)
        self.tracker = 0
        self.output_path = output_path
        self.font_folder = font_folder
        self.width = 600
        self.height = 100

    def get_fonts(self):
        fonts = os.listdir(self.font_folder)
        return fonts

    def get_font(self, font_name):
        ## Output
        output_path = os.path.join(self.output_path, font_name[:-4])
        if not os.path.exists(output_path):
            utils.make_dir(output_path)
        return os.path.join(self.font_folder, font_name), output_path

    def get_new_text(self):
        if self.tracker + 50 > len(self.cleaned_text):
            self.tracker = 0

        rd = np.random.randint(35, 40)
        rd += self.cleaned_text[self.tracker + rd:].find(" ")  # end on a space
        text = self.cleaned_text[self.tracker:self.tracker + rd]
        self.tracker += rd
        return text

    def clean_message(self,message):
        return re.sub('[^a-zA-Z,.?!;: ]', ' ', message)


    def check_size(self, txt, size):
        while font.getsize(txt)[0] > self.width:
            # iterate until the text size is just larger than the criteria
            size -= 2
            font = ImageFont.truetype("arial.ttf", size)

    def create_image(self, output_path, font_path, message, output_name=None,save=True):
        if output_name is None:
            output_name = message + ".png"
        if output_name[-4:] != ".png":
            output_name += ".png"

        # create Image object with the input image

        #image = Image.open('background.png')
        image = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))

        # initialise the drawing context with
        # the image object as background
        try:
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font_path, size=32) # 20, 32, 40, 48, 64, 96, 160
        except:
            return None
        # starting position of the message

        (x, y) = (10, 50)
        color = 'rgb(0, 0, 0)'  # black color

        # draw the message on the background
        draw.text((x, y), message, fill=color, font=font)

        # save the edited image
        if save:
            image.save(os.path.join(output_path, output_name))
            return True
        else:
            return image

    def create_next_image(self, font_name, save=True):
        text = tg.get_new_text()
        font_path, output_path = self.get_font(font_name)
        return self.create_image(output_path, font_path, text, save = save)

    def loop(self, save=True, n=1000):
        fonts = self.get_fonts()
        for i in range(0,n):
            font_name = fonts[i % len(fonts)]
            self.create_next_image(font_name, True)

if __name__ == '__main__':
    tg=TextGenerator(input_text_path = r"./text/tiny_shakespeare.txt", font_folder=r"./fonts/font_pack", output_path="./data")
    tg.loop()
