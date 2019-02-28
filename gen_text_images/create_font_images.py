# import required classes
import os
from PIL import Image, ImageDraw, ImageFont # pip install pillow
import re
import numpy as np
from gen_text_images import process_images
import utils
import multiprocessing

def open_file(path):
    with open(path, "r") as f:
        return "".join(f.readlines())

class TextGenerator():

    def __init__(self, input_text_path = r"./text/tiny_shakespeare.txt", font_folder=r"./fonts/font_pack", output_path="./data"):
        input_text = open_file(input_text_path)
        self.cleaned_text = self.clean_message(input_text)
        self.tracker = np.random.randint(0, len(self.cleaned_text))
        self.output_path = output_path
        self.font_folder = font_folder

        # Output image
        self.height = 64
        self.width = self.height*20
        self.font_size = 48

        # Generate message
        self.char_size_guess = 60
        self.char_size_variance = 0

    def get_fonts(self):
        fonts = os.listdir(self.font_folder)
        # fonts = fonts[0:100]
        # print(fonts)
        return fonts

    def get_font(self, font_name):
        ## Output
        output_path = os.path.join(self.output_path, font_name[:-4])
        if not os.path.exists(output_path):
            utils.make_dir(output_path)
        return os.path.join(self.font_folder, font_name), output_path

    def get_new_text(self, num_chars=50, variance=0):
        if self.tracker + self.char_size_guess > len(self.cleaned_text): # start over
            self.tracker = 0

        rd = np.random.randint(self.char_size_guess-self.char_size_variance, self.char_size_guess+self.char_size_variance) if self.char_size_variance !=0 else self.char_size_guess
        rd += self.cleaned_text[self.tracker + rd:].find(" ")  # end on a space
        text = self.cleaned_text[self.tracker:self.tracker + rd].strip()
        self.tracker += rd
        return text

    def clean_message(self,message):
        return re.sub('[^0-9a-zA-Z,.?!;: \'\%"]+', ' ', message)

    def trim_message(self, txt, font):
        while font.getsize(txt)[0] > self.width * 1.05:
            txt = self.delete_last_word(txt)
        return txt

    def delete_last_word(self, message):
        return message.rsplit(' ', 1)[0]

    def create_image(self, font_path, message):

        #image = Image.open('background.png')
        image = Image.new('L', (self.width, self.height), (255))
        #image = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))

        # initialise the drawing context with
        # the image object as background
        try:
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font_path, size=self.font_size) # 20, 32, 40, 48, 64, 96, 160
            message = self.trim_message(message, font)
        except:
            return None, None

        # starting position of the message
        (x, y) = (0, 0)
        color = 'rgb(0, 0, 0)'  # black color

        # draw the message on the background
        draw.text((x, y), message, fill=color, font=font)
        image = np.asarray(image)
        return image, message

    def save_PIL(self):
        image.save(os.path.join(output_path, output_name))

    def collect_result(self, result):
        print(result)
        return result

    def main(self, font_name, save=True):
        text = self.get_new_text()
        font_path, output_path = self.get_font(font_name)
        image, text = self.create_image(font_path, text)

        if image is None:
            return

        image = process_images.recrop_image(image, 100)
        image = process_images.resize_image(image, tolerance=1, pad_color=255, target_ratio=1 / 20.)

        # Save out
        if save:
            output_name = text + ".png"
            output_path = os.path.join(output_path, output_name)
            #output_path = os.path.join("./data", font_name + ".png")
            output_path = os.path.join("./data", output_name)
            process_images.save_image(output_path, image)
            return output_path
        else:
            return image

    def loop(self, save=True, n=4000000):

        fonts = self.get_fonts()
        for i in range(0,n):
            font_name = fonts[i % len(fonts)]
            try:
                self.main(font_name, True)
            except:
                print("Problem with {}".format(font_name))

def work(obj):
    obj.loop()

def multi(path):
    poolcount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=poolcount)
    print(poolcount)
    for p in range(0, poolcount):
        worker = TextGenerator(input_text_path = path, font_folder=root + r"/fonts/font_pack", output_path="./data")
        pool.apply_async(work, args=(worker,)) # , callback=self.collect_result)
    pool.close()
    pool.join()

def single(path):
    tg=TextGenerator(input_text_path = path, font_folder=root + r"/fonts/font_pack", output_path="./data")
    tg.loop()

if __name__ == '__main__':
    print(os.getcwd())
    root = "."
    path = root + r"/text/raw_text_10000.txt"
    multi(path)
    #single(path)

# rescale to a particular height
# add white space until
#fonts = ['SF Arch Rival Bold.ttf', 'Exo-Black.otf', 'criticized.ttf', 'corbelb.ttf', 'AVENGEANCE MIGHTIEST AVENGER.otf', '8bitlim.ttf', 'BankGothic-Regular DB.ttf', 'Colors Of Autumn.ttf', 'ALIEESBI.TTF', 'Harabara.ttf', 'Moon Flower Bold.ttf', 'Delicious-BoldItalic.otf', 'CHICSA__.TTF', 'Existence-Light.otf', 'InversionzUnboxed.otf', 'NFS_by_JLTV.ttf', 'PoplarStd.otf', 'Snowstorm Kraft.ttf', 'Korner Deli NF.ttf', 'ARMOPB__.TTF', 'Diavlo_BOOK_II.otf', 'kirsty__.ttf', 'YARDSALE.TTF', 'distortion_of_the_brain_and_mind.ttf', 'SF Sports Night NS.ttf', 'SelznickNormal.ttf', 'Tall Film.ttf', 'couture-bld.otf', 'ADD-JAZZ.TTF', 'libelsuit.ttf', 'Delicious-Heavy.otf', 'VISITOR.FON', 'verdanab.ttf', 'bluehigh.ttf', 'MankSans-Medium.ttf', 'AliquamREG.ttf', 'BEBAS.TTF', 'Vegur-B 0.602.otf', 'AdobeHeitiStd-Regular.otf', 'KataBidalanBold.ttf', 'SF Toontime B.ttf', 'Ancillary-Bold.otf', 'NirmalaB.ttf', 'Aileenation.ttf', 'BEDOUIN.otf', 'SF Foxboro Script Bold.ttf', 'LOVEA___.TTF', 'Delicious-Roman.otf', 'Something Strange.ttf', 'TalkingToTheMoon.ttf', 'Minecraftia-Regular.ttf', 'X-rayTed_s.TTF', 'ABBERANC.TTF', 'Florsn02.ttf', 'COUTURE-Bold.ttf', 'impact.ttf', 'SamdanCondensed.ttf', 'ClearLine_PERSONAL_USE_ONLY.ttf', 'Diavlo_BOLD_II.otf', 'DIMITRI_.TTF', 'Call of Ops Duty.otf', 'Advokat Modern.ttf', 'overhead.ttf', 'UltraCondensedSansSerif.ttf', 'chinese rocks rg.ttf', 'ratio___.ttf', 'wyldb.ttf', 'viva01.ttf', 'CHINESER.ttf', 'Diavlo_BLACK_II.otf', 'KENYAN.TTF', 'Vegetable.ttf', 'Aliquamulti.ttf', 'BUBBLEBO.TTF', 'BEBAS__.TTF', 'Atlantic_Cruise-Demo.ttf', 'RADIOSTA.TTF', 'SOVIET4.TTF', 'Comicv2b.ttf', 'SF Juggernaut Condensed.ttf', 'Deadly Inked.ttf', 'corbelz.ttf', 'Alice and the Wicked Monster.ttf', 'Snowstorm Kraft_0.ttf', 'SF Willamette.ttf', 'BabelSans-Bold.ttf', 'UNICORN.TTF', 'light.otf', 'SF Grunge Sans Bold Italic.ttf', 'BOTTRBB_.TTF', 'steelfis.ttf', 'YELBM.FON', 'CHICM___.TTF', 'Vanadine Bold.ttf', 'YanoneKaffeesatz-Regular.ttf', 'visitor2.ttf', 'SF Grunge Sans SC.ttf', 'segoeuib.ttf', 'srgt6pack.ttf', 'BNMachine.ttf']
#fonts = ["Ubuntu-B", "tahoma",
